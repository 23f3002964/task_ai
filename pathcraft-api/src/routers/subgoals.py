from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    tags=["Sub-Goals"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/goals/{goal_id}/subgoals/",
    response_model=schemas.SubGoal,
    status_code=status.HTTP_201_CREATED,
)
def create_sub_goal_for_goal(
    goal_id: UUID, sub_goal: schemas.SubGoalCreate, db: Session = Depends(get_db)
):
    """
    Create a new sub-goal for a specific goal.
    """
    # First, check if the parent goal exists
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Parent goal not found")
    return crud.create_sub_goal(db=db, sub_goal=sub_goal, goal_id=goal_id)


@router.get("/goals/{goal_id}/subgoals/", response_model=List[schemas.SubGoal])
def read_sub_goals_for_goal(
    goal_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retrieve all sub-goals for a specific goal.
    """
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Parent goal not found")

    sub_goals = crud.get_sub_goals_by_goal(db, goal_id=goal_id, skip=skip, limit=limit)
    return sub_goals


@router.get("/subgoals/{sub_goal_id}", response_model=schemas.SubGoal)
def read_single_sub_goal(sub_goal_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a single sub-goal by its ID.
    """
    db_sub_goal = crud.get_sub_goal(db, sub_goal_id=sub_goal_id)
    if db_sub_goal is None:
        raise HTTPException(status_code=404, detail="Sub-goal not found")
    return db_sub_goal


@router.put("/subgoals/{sub_goal_id}", response_model=schemas.SubGoal)
def update_existing_sub_goal(
    sub_goal_id: UUID, sub_goal_in: schemas.SubGoalUpdate, db: Session = Depends(get_db)
):
    """
    Update a sub-goal's details.
    """
    db_sub_goal = crud.get_sub_goal(db, sub_goal_id=sub_goal_id)
    if db_sub_goal is None:
        raise HTTPException(status_code=404, detail="Sub-goal not found")

    return crud.update_sub_goal(db=db, db_sub_goal=db_sub_goal, sub_goal_in=sub_goal_in)


@router.delete("/subgoals/{sub_goal_id}", response_model=schemas.SubGoal)
def delete_existing_sub_goal(sub_goal_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a sub-goal by its ID.
    """
    db_sub_goal = crud.get_sub_goal(db, sub_goal_id=sub_goal_id)
    if db_sub_goal is None:
        raise HTTPException(status_code=404, detail="Sub-goal not found")

    return crud.delete_sub_goal(db, sub_goal_id=sub_goal_id)
