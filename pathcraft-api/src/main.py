from fastapi import FastAPI

from . import models
from .database import engine
from .routers import goals

# This line creates the database tables based on the models defined in models.py
# It will create the 'pathcraft.db' file in the root directory if it doesn't exist.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PathCraft API",
    description="API for the PathCraft goal-setting and productivity application.",
    version="0.1.0 (MVP Phase 1)",
)

# Include the router for goal-related endpoints
app.include_router(goals.router)


@app.get("/", tags=["Health Check"])
def read_root():
    """
    A health check endpoint to confirm the API is running.
    """
    return {"status": "ok", "message": "Welcome to the PathCraft API!"}
