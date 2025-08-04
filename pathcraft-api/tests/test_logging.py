import pytest
from fastapi.testclient import TestClient
from src.schemas import UserCreate, ExperimentCreate

def test_create_metric(client: TestClient, test_user: dict, test_experiment: dict):
    response = client.post(
        "/logging/metrics",
        json={
            "name": "test_metric",
            "value": 1,
            "user_id": test_user["id"],
            "experiment_id": test_experiment["id"],
            "group": "control",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test_metric"
    assert data["value"] == 1
    assert data["user_id"] == test_user["id"]
    assert data["experiment_id"] == test_experiment["id"]
    assert data["group"] == "control"

def test_create_log(client: TestClient, test_user: dict):
    response = client.post(
        "/logging/logs",
        json={"event": "test_event", "user_id": test_user["id"], "details": {"foo": "bar"}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["event"] == "test_event"
    assert data["user_id"] == test_user["id"]
    assert data["details"] == {"foo": "bar"}
