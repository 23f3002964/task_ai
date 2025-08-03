# PathCraft API

This is the backend API for **Project Codename: PathCraft**, a goal-setting and productivity application that blends goal-setting science with artificial-intelligence scheduling. This API is responsible for goal management, decomposition, scheduling, and user data persistence.

This service is built with Python using the [FastAPI](https://fastapi.tiangolo.com/) web framework and [SQLAlchemy](https://www.sqlalchemy.org/) for the ORM.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.12+
- `pip` and `venv`

### Setup and Installation

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository-url>
    cd pathcraft-api
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    # On Windows, use: venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install the development dependencies (for testing):**
    ```bash
    pip install -r requirements-dev.txt
    ```

### Running the Application

To run the API server locally, use `uvicorn`:

```bash
uvicorn src.main:app --reload
```

The `--reload` flag makes the server restart after code changes. The API will be available at `http://127.0.0.1:8000`.

### Running Tests

To run the test suite, use `pytest` from the `pathcraft-api` root directory:

```bash
pytest
```

## API Documentation

Once the application is running, you can access the interactive API documentation (provided by Swagger UI) at:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

An alternative documentation view (provided by ReDoc) is available at:

[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Project Structure

```
pathcraft-api/
├── src/
│   ├── __init__.py
│   ├── main.py         # FastAPI application entry point
│   └── models.py       # SQLAlchemy database models
├── tests/
│   ├── __init__.py
│   └── test_main.py    # Tests for the main application
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development/test dependencies
└── README.md             # This file
```
