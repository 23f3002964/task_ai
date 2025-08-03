from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    tags=["Tasks"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/subgoals/{subgoal_id}/tasks/",
    response_model=schemas.Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a Task for a Sub-Goal",
)
def create_task_for_subgoal(
    subgoal_id: UUID, task: schemas.TaskCreate, db: Session = Depends(get_db)
):
    """
    Create a new task for a specific sub-goal.
    """
    # Check if the parent sub-goal exists
    db_subgoal = crud.get_sub_goal(db, sub_goal_id=subgoal_id)
    if db_subgoal is None:
        raise HTTPException(status_code=404, detail="Parent sub-goal not found")

    return crud.create_task(db=db, task=task, sub_goal_id=subgoal_id)


@router.get(
    "/subgoals/{subgoal_id}/tasks/",
    response_model=List[schemas.Task],
    summary="Read Tasks for a Sub-Goal",
)
def read_tasks_for_subgoal(
    subgoal_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retrieve all tasks for a specific sub-goal.
    """
    db_subgoal = crud.get_sub_goal(db, sub_goal_id=subgoal_id)
    if db_subgoal is None:
        raise HTTPException(status_code=404, detail="Parent sub-goal not found")

    tasks = crud.get_tasks_by_sub_goal(
        db, sub_goal_id=subgoal_id, skip=skip, limit=limit
    )
    return tasks


@router.get(
    "/tasks/{task_id}", response_model=schemas.Task, summary="Read a Single Task"
)
def read_single_task(task_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a single task by its ID.
    """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/tasks/{task_id}", response_model=schemas.Task, summary="Update a Task")
def update_existing_task(
    task_id: UUID, task_in: schemas.TaskUpdate, db: Session = Depends(get_db)
):
    """
    Update a task's details.
    """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return crud.update_task(db=db, db_task=db_task, task_in=task_in)


@router.delete("/tasks/{task_id}", response_model=schemas.Task, summary="Delete a Task")
def delete_existing_task(task_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a task by its ID.
    """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return crud.delete_task(db, task_id=task_id)
