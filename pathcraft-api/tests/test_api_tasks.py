from fastapi.testclient import TestClient
from datetime import datetime, timezone, timedelta

# Note: Fixtures `client` and `test_sub_goal` are defined in `conftest.py`

# ====================
# Task API Tests
# ====================


def test_create_task_for_subgoal(client: TestClient, test_sub_goal: dict):
    """
    Test creating a new task for an existing sub-goal.
    """
    subgoal_id = test_sub_goal["id"]
    start_time = datetime.now(timezone.utc).isoformat()
    end_time = datetime.now(timezone.utc).isoformat()

    response = client.post(
        f"/subgoals/{subgoal_id}/tasks/",
        json={
            "description": "First task",
            "planned_start": start_time,
            "planned_end": end_time,
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["description"] == "First task"
    assert data["subgoal_id"] == subgoal_id
    assert data["status"] == "todo"  # Default status
    assert "id" in data


def test_read_tasks_for_subgoal(client: TestClient, test_sub_goal: dict):
    """
    Test retrieving all tasks for a specific sub-goal.
    """
    subgoal_id = test_sub_goal["id"]
    # Create a couple of tasks
    client.post(f"/subgoals/{subgoal_id}/tasks/", json={"description": "Task 1"})
    client.post(f"/subgoals/{subgoal_id}/tasks/", json={"description": "Task 2"})

    response = client.get(f"/subgoals/{subgoal_id}/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["description"] == "Task 1"
    assert data[1]["description"] == "Task 2"


def test_read_single_task(client: TestClient, test_sub_goal: dict):
    """
    Test retrieving a single task by its own ID.
    """
    subgoal_id = test_sub_goal["id"]
    create_response = client.post(
        f"/subgoals/{subgoal_id}/tasks/", json={"description": "A specific task"}
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "A specific task"
    assert data["id"] == task_id


def test_update_task(client: TestClient, test_sub_goal: dict):
    """
    Test updating an existing task's details, like its status.
    """
    subgoal_id = test_sub_goal["id"]
    create_response = client.post(
        f"/subgoals/{subgoal_id}/tasks/", json={"description": "Original description"}
    )
    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"description": "Updated description", "status": "in-progress"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated description"
    assert data["status"] == "in-progress"


def test_delete_task(client: TestClient, test_sub_goal: dict):
    """
    Test deleting a task.
    """
    subgoal_id = test_sub_goal["id"]
    create_response = client.post(
        f"/subgoals/{subgoal_id}/tasks/", json={"description": "To be deleted"}
    )
    task_id = create_response.json()["id"]

    # Delete the task
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == task_id

    # Verify it's gone
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_get_schedule_for_date_range(client: TestClient, test_sub_goal: dict):
    """
    Test the GET /schedule endpoint for fetching tasks within a date range.
    """
    subgoal_id = test_sub_goal["id"]
    now = datetime.now(timezone.utc)
    today = now.date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    # Create tasks with different planned_start dates
    client.post(
        f"/subgoals/{subgoal_id}/tasks/",
        json={"description": "Task Yesterday", "planned_start": (now - timedelta(days=1)).isoformat()}
    )
    client.post(
        f"/subgoals/{subgoal_id}/tasks/",
        json={"description": "Task Today", "planned_start": now.isoformat()}
    )
    client.post(
        f"/subgoals/{subgoal_id}/tasks/",
        json={"description": "Task Tomorrow", "planned_start": (now + timedelta(days=1)).isoformat()}
    )

    # Test fetching tasks just for today
    response_today = client.get(f"/schedule/?start_date={today}&end_date={today}")
    assert response_today.status_code == 200
    data_today = response_today.json()
    assert len(data_today) == 1
    assert data_today[0]["description"] == "Task Today"

    # Test fetching tasks for a range including all three tasks
    response_range = client.get(f"/schedule/?start_date={yesterday}&end_date={tomorrow}")
    assert response_range.status_code == 200
    data_range = response_range.json()
    assert len(data_range) == 3

    # Test fetching tasks for a range with no tasks
    far_future = today + timedelta(days=10)
    response_empty = client.get(f"/schedule/?start_date={far_future}&end_date={far_future}")
    assert response_empty.status_code == 200
    assert len(response_empty.json()) == 0
