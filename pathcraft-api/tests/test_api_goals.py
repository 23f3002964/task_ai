import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timezone

from src.main import app
from src.database import get_db
from src.models import Base

# ====================
# Test Setup
# ====================

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Use a static pool for in-memory DB
)

# Create a new sessionmaker for the test database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pytest fixture to set up and tear down the database for each test
@pytest.fixture(scope="function")
def db_session():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables
        Base.metadata.drop_all(bind=engine)

# Pytest fixture to provide a TestClient with the get_db dependency overridden
@pytest.fixture(scope="function")
def client(db_session: Session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Clean up the dependency override
    del app.dependency_overrides[get_db]

# ====================
# API Tests
# ====================

from datetime import timedelta

def test_create_goal(client: TestClient):
    """
    Test creating a new goal via the POST /goals endpoint.
    """
    target_date = datetime.now(timezone.utc)
    response = client.post(
        "/goals/",
        json={"title": "Learn FastAPI", "target_date": target_date.isoformat()},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == "Learn FastAPI"

    # Compare datetime objects for robustness, assuming UTC if the response is naive.
    response_date = datetime.fromisoformat(data["target_date"])
    if response_date.tzinfo is None:
        response_date = response_date.replace(tzinfo=timezone.utc)

    assert abs(response_date - target_date) < timedelta(seconds=1)

    assert "id" in data
    assert data["methodology"] == "custom"

def test_read_goals(client: TestClient, db_session: Session):
    """
    Test retrieving a list of goals via the GET /goals endpoint.
    """
    # Create some goals first
    target_date_str = datetime.now(timezone.utc).isoformat()
    client.post("/goals/", json={"title": "Goal 1", "target_date": target_date_str})
    client.post("/goals/", json={"title": "Goal 2", "target_date": target_date_str})

    response = client.get("/goals/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Goal 1"
    assert data[1]["title"] == "Goal 2"

def test_read_single_goal(client: TestClient):
    """
    Test retrieving a single goal by its ID.
    """
    target_date_str = datetime.now(timezone.utc).isoformat()
    create_response = client.post(
        "/goals/",
        json={"title": "Specific Goal", "target_date": target_date_str},
    )
    goal_id = create_response.json()["id"]

    read_response = client.get(f"/goals/{goal_id}")
    assert read_response.status_code == 200
    data = read_response.json()
    assert data["title"] == "Specific Goal"
    assert data["id"] == goal_id

def test_update_goal(client: TestClient):
    """
    Test updating an existing goal.
    """
    target_date_str = datetime.now(timezone.utc).isoformat()
    create_response = client.post(
        "/goals/",
        json={"title": "Original Title", "target_date": target_date_str},
    )
    goal_id = create_response.json()["id"]

    update_response = client.put(
        f"/goals/{goal_id}",
        json={"title": "Updated Title"},
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["title"] == "Updated Title"
    assert data["id"] == goal_id

def test_delete_goal(client: TestClient):
    """
    Test deleting a goal.
    """
    target_date_str = datetime.now(timezone.utc).isoformat()
    create_response = client.post(
        "/goals/",
        json={"title": "To Be Deleted", "target_date": target_date_str},
    )
    goal_id = create_response.json()["id"]

    # Delete the goal
    delete_response = client.delete(f"/goals/{goal_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == goal_id

    # Verify it's gone
    get_response = client.get(f"/goals/{goal_id}")
    assert get_response.status_code == 404

def test_read_nonexistent_goal(client: TestClient):
    """
    Test that reading a non-existent goal returns a 404 error.
    """
    import uuid
    non_existent_id = uuid.uuid4()
    response = client.get(f"/goals/{non_existent_id}")
    assert response.status_code == 404
