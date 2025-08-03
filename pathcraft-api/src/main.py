from fastapi import FastAPI

app = FastAPI(
    title="PathCraft API",
    description="API for the PathCraft goal-setting and productivity application.",
    version="0.1.0 (MVP Phase 1)",
)

@app.get("/")
def read_root():
    """A health check endpoint to confirm the API is running."""
    return {"status": "ok", "message": "Welcome to the PathCraft API!"}
