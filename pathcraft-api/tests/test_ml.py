import pytest
from fastapi.testclient import TestClient
from src.ml.slot_selector import SlotSelector, get_dummy_data
from src.ml.calendar_optimizer import CalendarOptimizer
import numpy as np
from datetime import datetime, timedelta

def test_slot_selector():
    selector = SlotSelector()
    X_train, y_train = get_dummy_data()
    selector.train(X_train, y_train)
    X_test = np.array([[10, 2], [18, 5]])
    predictions = selector.predict(X_test)
    probabilities = selector.predict_proba(X_test)
    assert len(predictions) == 2
    assert len(probabilities) == 2

def test_calendar_optimizer():
    tasks = [{'name': 'Task 1', 'duration': 2}, {'name': 'Task 2', 'duration': 1}]
    now = datetime.now()
    slots = [{'name': 'Slot A', 'start': now, 'end': now + timedelta(hours=3)}, {'name': 'Slot B', 'start': now + timedelta(hours=4), 'end': now + timedelta(hours=6)}]
    optimizer = CalendarOptimizer(tasks, slots)
    solution = optimizer.optimize()
    assert solution is not None
    assert 'Slot A' in solution
    assert 'Slot B' in solution
    assert 'Task 1' in solution['Slot A'] or 'Task 1' in solution['Slot B']
    assert 'Task 2' in solution['Slot A'] or 'Task 2' in solution['Slot B']

def test_optimize_schedule_endpoint(client: TestClient, test_goal: dict):
    # Create a sub-goal
    sub_goal_response = client.post(
        f"/goals/{test_goal['id']}/subgoals/",
        json={"description": "Test Sub-Goal for ML", "estimated_effort_minutes": 60},
    )
    sub_goal_id = sub_goal_response.json()["id"]

    # Create some tasks for the sub-goal
    task1_response = client.post(
        f"/subgoals/{sub_goal_id}/tasks/", json={"description": "Task 1 for ML"}
    )
    task2_response = client.post(
        f"/subgoals/{sub_goal_id}/tasks/", json={"description": "Task 2 for ML"}
    )
    task1_id = task1_response.json()["id"]
    task2_id = task2_response.json()["id"]

    # Define available time slots
    now = datetime.now()
    available_slots = [
        {"start": (now + timedelta(hours=1)).isoformat(), "end": (now + timedelta(hours=2)).isoformat()},
        {"start": (now + timedelta(hours=3)).isoformat(), "end": (now + timedelta(hours=4)).isoformat()},
    ]

    # Call the optimizer endpoint
    response = client.post(
        "/ml/schedule/optimize",
        json={"task_ids": [task1_id, task2_id], "available_slots": available_slots},
    )
    assert response.status_code == 200
    data = response.json()
    assert "optimized_slots" in data
    assert len(data["optimized_slots"]) > 0
    # Further assertions can be made here to check the correctness of the solution

def test_reminder_suggestion_endpoint(client: TestClient):
    response = client.post("/ml/reminders/suggest", json={"user_id": "test_user"})
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user"
    assert "suggestion" in data

def test_reminder_reward_endpoint(client: TestClient):
    response = client.post(
        "/ml/reminders/reward",
        json={"user_id": "test_user", "arm": "push_15_min", "reward": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
