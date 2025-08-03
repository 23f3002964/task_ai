import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timezone

from src.main import app
from src.database import get_db
from src.models import Base

# ====================
# Test Fixtures
# ====================

# Use an in-memory SQLite database for all tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create a new sessionmaker for the test database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Pytest fixture to set up and tear down the database for each test function.
    This ensures that each test runs on a clean database.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session: Session):
    """
    Pytest fixture to provide a TestClient with the get_db dependency overridden.
    This allows tests to interact with the in-memory test database.
    """
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Clean up the dependency override after the test
    del app.dependency_overrides[get_db]

# Helper fixture to create a goal for tests that need one
@pytest.fixture(scope="function")
def test_goal(client: TestClient) -> dict:
    """
    Pytest fixture to create a single goal and return its data.
    """
    target_date_str = datetime.now(timezone.utc).isoformat()
    response = client.post(
        "/goals/",
        json={"title": "Test Parent Goal", "target_date": target_date_str},
    )
    assert response.status_code == 201
    return response.json()

@pytest.fixture(scope="function")
def test_sub_goal(client: TestClient, test_goal: dict) -> dict:
    """
    Pytest fixture to create a single sub-goal under the test_goal.
    """
    goal_id = test_goal["id"]
    response = client.post(
        f"/goals/{goal_id}/subgoals/",
        json={"description": "Test Sub-Goal"},
    )
    assert response.status_code == 201
    return response.json()
