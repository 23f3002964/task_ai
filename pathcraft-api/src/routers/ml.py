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
