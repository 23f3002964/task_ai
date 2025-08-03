from fastapi.testclient import TestClient

# Note: Fixtures `client` and `test_goal` are defined in `conftest.py`

# =======================
# Sub-Goal API Tests
# =======================

def test_create_sub_goal_for_goal(client: TestClient, test_goal: dict):
    """
    Test creating a new sub-goal for an existing goal.
    """
    goal_id = test_goal["id"]
    response = client.post(
        f"/goals/{goal_id}/subgoals/",
        json={"description": "First sub-goal", "estimated_effort_minutes": 60},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["description"] == "First sub-goal"
    assert data["estimated_effort_minutes"] == 60
    assert data["parent_goal_id"] == goal_id
    assert "id" in data

def test_create_sub_goal_for_nonexistent_goal(client: TestClient):
    """
    Test that creating a sub-goal for a non-existent goal fails.
    """
    import uuid
    non_existent_goal_id = uuid.uuid4()
    response = client.post(
        f"/goals/{non_existent_goal_id}/subgoals/",
        json={"description": "This should fail"},
    )
    assert response.status_code == 404

def test_read_sub_goals_for_goal(client: TestClient, test_goal: dict):
    """
    Test retrieving all sub-goals for a specific goal.
    """
    goal_id = test_goal["id"]
    # Create a couple of sub-goals
    client.post(f"/goals/{goal_id}/subgoals/", json={"description": "Sub-goal 1"})
    client.post(f"/goals/{goal_id}/subgoals/", json={"description": "Sub-goal 2"})

    response = client.get(f"/goals/{goal_id}/subgoals/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["description"] == "Sub-goal 1"
    assert data[1]["description"] == "Sub-goal 2"

def test_read_single_sub_goal(client: TestClient, test_goal: dict):
    """
    Test retrieving a single sub-goal by its own ID.
    """
    goal_id = test_goal["id"]
    create_response = client.post(
        f"/goals/{goal_id}/subgoals/", json={"description": "A specific sub-goal"}
    )
    sub_goal_id = create_response.json()["id"]

    response = client.get(f"/subgoals/{sub_goal_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "A specific sub-goal"
    assert data["id"] == sub_goal_id

def test_update_sub_goal(client: TestClient, test_goal: dict):
    """
    Test updating an existing sub-goal.
    """
    goal_id = test_goal["id"]
    create_response = client.post(
        f"/goals/{goal_id}/subgoals/", json={"description": "Original description"}
    )
    sub_goal_id = create_response.json()["id"]

    response = client.put(
        f"/subgoals/{sub_goal_id}", json={"description": "Updated description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated description"

def test_delete_sub_goal(client: TestClient, test_goal: dict):
    """
    Test deleting a sub-goal.
    """
    goal_id = test_goal["id"]
    create_response = client.post(
        f"/goals/{goal_id}/subgoals/", json={"description": "To be deleted"}
    )
    sub_goal_id = create_response.json()["id"]

    # Delete the sub-goal
    delete_response = client.delete(f"/subgoals/{sub_goal_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == sub_goal_id

    # Verify it's gone
    get_response = client.get(f"/subgoals/{sub_goal_id}")
    assert get_response.status_code == 404
