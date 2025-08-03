from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas, decomposition
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

@router.post(
    "/{goal_id}/decompose",
    response_model=List[schemas.SubGoal],
    status_code=status.HTTP_201_CREATED,
    summary="Decompose Goal into Sub-Goals",
)
def decompose_goal_and_create_sub_goals(
    goal_id: UUID, db: Session = Depends(get_db)
):
    """
    Automatically decompose a goal into a set of sub-goals based on predefined templates.

    This endpoint will:
    1. Find the parent goal.
    2. Use the decomposition service to generate a list of sub-goals.
    3. If a template is found, create and save the new sub-goals.
    4. Return the list of newly created sub-goals.
    """
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")

    sub_goals_to_create = decomposition.decompose_goal(db_goal)
    if not sub_goals_to_create:
        raise HTTPException(
            status_code=400,
            detail=f"Could not decompose goal: No matching template found for title '{db_goal.title}'.",
        )

    created_sub_goals = [
        crud.create_sub_goal(db=db, sub_goal=sub_goal_schema, goal_id=goal_id)
        for sub_goal_schema in sub_goals_to_create
    ]

    return created_sub_goals

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
