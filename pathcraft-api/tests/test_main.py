from fastapi.testclient import TestClient

# When running pytest from the 'pathcraft-api' root, it should find the 'src' module.
from src.main import app

# Create a client to interact with the API
client = TestClient(app)


def test_read_root_health_check():
    """
    Tests that the root endpoint returns a 200 OK status and the expected welcome message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "Welcome to the PathCraft API!",
    }
