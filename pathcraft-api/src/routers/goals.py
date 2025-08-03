from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/goals",
    tags=["Goals"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Goal, status_code=status.HTTP_201_CREATED)
def create_new_goal(goal: schemas.GoalCreate, db: Session = Depends(get_db)):
    """
    Create a new goal.
    """
    return crud.create_goal(db=db, goal=goal)

@router.get("/", response_model=List[schemas.Goal])
def read_all_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all goals with pagination.
    """
    goals = crud.get_goals(db, skip=skip, limit=limit)
    return goals

@router.get("/{goal_id}", response_model=schemas.Goal)
def read_single_goal(goal_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a single goal by its ID.
    """
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return db_goal

@router.put("/{goal_id}", response_model=schemas.Goal)
def update_existing_goal(
    goal_id: UUID, goal_in: schemas.GoalUpdate, db: Session = Depends(get_db)
):
    """
    Update a goal's details.
    """
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    updated_goal = crud.update_goal(db=db, db_goal=db_goal, goal_in=goal_in)
    return updated_goal

@router.delete("/{goal_id}", response_model=schemas.Goal)
def delete_existing_goal(goal_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a goal by its ID.
    """
    db_goal = crud.delete_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return db_goal
