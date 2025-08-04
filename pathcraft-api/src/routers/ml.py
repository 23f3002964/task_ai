from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from ..ml.slot_selector import SlotSelector, get_dummy_data
from ..ml.calendar_optimizer import CalendarOptimizer
import numpy as np

router = APIRouter()

# In a real application, the model would be trained and loaded once, not on every request.
# For this example, we'll train it on dummy data each time.
slot_selector = SlotSelector()
X_train, y_train = get_dummy_data()
slot_selector.train(X_train, y_train)

from ..ml.reminder_system import ReminderBanditManager

reminder_manager = ReminderBanditManager()

from .. import ab_testing

@router.post("/reminders/suggest", response_model=schemas.ReminderSuggestion)
def suggest_reminder(suggestion_request: schemas.ReminderSuggestionRequest, db: Session = Depends(get_db)):
    """
    Suggests a reminder strategy for a given user.
    """
    user = crud.get_user(db, user_id=suggestion_request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    experiment = crud.get_experiment_by_name(db, name="reminder_test")
    if not experiment:
        # If no experiment is running, use the default bandit
        arms = ['push_15_min', 'email_1_hour', 'sms_on_day']
        bandit = reminder_manager.get_bandit(user_id=suggestion_request.user_id, arms=arms)
        suggestion = bandit.select_arm()
        return schemas.ReminderSuggestion(user_id=suggestion_request.user_id, suggestion=suggestion)

    group = ab_testing.get_user_group(user, experiment)
    crud.update_user(db, user) # To save the user's group if it was just assigned

    if group == "treatment":
        # In a real application, this would be a different reminder strategy
        return schemas.ReminderSuggestion(user_id=suggestion_request.user_id, suggestion="sms_5_min")
    else: # control group
        arms = ['push_15_min', 'email_1_hour', 'sms_on_day']
        bandit = reminder_manager.get_bandit(user_id=suggestion_request.user_id, arms=arms)
        suggestion = bandit.select_arm()
        return schemas.ReminderSuggestion(user_id=suggestion_request.user_id, suggestion=suggestion)

@router.post("/reminders/reward")
def reward_reminder(reward_request: schemas.ReminderReward):
    """
    Updates the reminder bandit with a reward.
    """
    arms = ['push_15_min', 'email_1_hour', 'sms_on_day']
    bandit = reminder_manager.get_bandit(user_id=reward_request.user_id, arms=arms)
    bandit.update(arm=reward_request.arm, reward=reward_request.reward)
    reminder_manager.save_bandit(bandit)
    return {"status": "ok"}

@router.post("/schedule/optimize", response_model=schemas.Schedule)
def optimize_schedule(schedule_request: schemas.ScheduleRequest, db: Session = Depends(get_db)):
    """
    Optimizes the schedule for a given set of tasks and available time slots.
    """
    # 1. Get tasks from the database
    tasks_with_duration = []
    for task_id in schedule_request.task_ids:
        task = crud.get_task(db, task_id)
        if task:
            sub_goal = crud.get_sub_goal(db, task.subgoal_id)
            if sub_goal and sub_goal.estimated_effort_minutes and len(sub_goal.tasks) > 0:
                duration = int(sub_goal.estimated_effort_minutes / len(sub_goal.tasks))
            else:
                duration = 30  # Default duration if not specified
            tasks_with_duration.append({"id": task.id, "name": task.description, "duration": duration})

    # 2. Get available slots from the request
    slots = [{"name": f"Slot {i}", "start": slot.start, "end": slot.end} for i, slot in enumerate(schedule_request.available_slots)]

    # 3. Use the SlotSelector to predict the best slots
    # This is a simplified example. In a real application, you would create features
    # for each slot and predict its productivity.
    slot_features = np.array([[slot['start'].hour, slot['start'].weekday()] for slot in slots])
    slot_probabilities = slot_selector.predict_proba(slot_features)[:, 1]

    # 4. Use the CalendarOptimizer to assign tasks to slots
    # We can use the slot probabilities as a preference for the optimizer.
    # This is a simplified example. A more complex implementation would incorporate
    # the probabilities into the optimization objective.
    optimizer = CalendarOptimizer(tasks_with_duration, slots)
    solution = optimizer.optimize()

    if solution:
        # 5. Format the solution into the response model
        optimized_slots = []
        for slot_name, assigned_tasks in solution.items():
            slot_info = next((s for s in schedule_request.available_slots if f"Slot {schedule_request.available_slots.index(s)}" == slot_name), None)
            if slot_info:
                assigned_task_ids = []
                for task_name in assigned_tasks:
                    task_info = next((t for t in tasks_with_duration if t['name'] == task_name), None)
                    if task_info:
                        assigned_task_ids.append(task_info['id'])
                optimized_slots.append(schemas.OptimizedSlot(start=slot_info.start, end=slot_info.end, task_ids=assigned_task_ids))
        return schemas.Schedule(optimized_slots=optimized_slots)
    else:
        return {"optimized_slots": []}
