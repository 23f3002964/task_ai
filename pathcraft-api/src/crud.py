from uuid import UUID
from sqlalchemy.orm import Session
from . import models, schemas

# ====================
# Goal CRUD Functions
# ====================

def get_goal(db: Session, goal_id: UUID) -> models.Goal | None:
    """
    Retrieve a single goal by its ID.
    """
    return db.query(models.Goal).filter(models.Goal.id == goal_id).first()

def get_goals(db: Session, skip: int = 0, limit: int = 100) -> list[models.Goal]:
    """
    Retrieve a list of goals with pagination.
    """
    return db.query(models.Goal).offset(skip).limit(limit).all()

def create_goal(db: Session, goal: schemas.GoalCreate) -> models.Goal:
    """
    Create a new goal in the database.
    """
    # Create a new Goal model instance from the Pydantic schema
    db_goal = models.Goal(**goal.model_dump())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def update_goal(
    db: Session, db_goal: models.Goal, goal_in: schemas.GoalUpdate
) -> models.Goal:
    """
    Update an existing goal in the database.
    """
    update_data = goal_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_goal, key, value)

    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def delete_goal(db: Session, goal_id: UUID) -> models.Goal | None:
    """
    Delete a goal from the database by its ID.
    """
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if db_goal:
        db.delete(db_goal)
        db.commit()
    return db_goal

# =======================
# Sub-Goal CRUD Functions
# =======================

def get_sub_goal(db: Session, sub_goal_id: UUID) -> models.SubGoal | None:
    """
    Retrieve a single sub-goal by its ID.
    """
    return db.query(models.SubGoal).filter(models.SubGoal.id == sub_goal_id).first()

def get_sub_goals_by_goal(db: Session, goal_id: UUID, skip: int = 0, limit: int = 100) -> list[models.SubGoal]:
    """
    Retrieve a list of sub-goals for a specific goal with pagination.
    """
    return db.query(models.SubGoal).filter(models.SubGoal.parent_goal_id == goal_id).offset(skip).limit(limit).all()

def create_sub_goal(db: Session, sub_goal: schemas.SubGoalCreate, goal_id: UUID) -> models.SubGoal:
    """
    Create a new sub-goal for a given goal.
    """
    db_sub_goal = models.SubGoal(**sub_goal.model_dump(), parent_goal_id=goal_id)
    db.add(db_sub_goal)
    db.commit()
    db.refresh(db_sub_goal)
    return db_sub_goal

def update_sub_goal(
    db: Session, db_sub_goal: models.SubGoal, sub_goal_in: schemas.SubGoalUpdate
) -> models.SubGoal:
    """
    Update an existing sub-goal.
    """
    update_data = sub_goal_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sub_goal, key, value)

    db.add(db_sub_goal)
    db.commit()
    db.refresh(db_sub_goal)
    return db_sub_goal

def delete_sub_goal(db: Session, sub_goal_id: UUID) -> models.SubGoal | None:
    """
    Delete a sub-goal from the database by its ID.
    """
    db_sub_goal = db.query(models.SubGoal).filter(models.SubGoal.id == sub_goal_id).first()
    if db_sub_goal:
        db.delete(db_sub_goal)
        db.commit()
    return db_sub_goal

# ====================
# Task CRUD Functions
# ====================

def get_task(db: Session, task_id: UUID) -> models.Task | None:
    """
    Retrieve a single task by its ID.
    """
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks_by_sub_goal(
    db: Session, sub_goal_id: UUID, skip: int = 0, limit: int = 100
) -> list[models.Task]:
    """
    Retrieve a list of tasks for a specific sub-goal with pagination.
    """
    return (
        db.query(models.Task)
        .filter(models.Task.subgoal_id == sub_goal_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_task(db: Session, task: schemas.TaskCreate, sub_goal_id: UUID) -> models.Task:
    """
    Create a new task for a given sub-goal.
    """
    db_task = models.Task(**task.model_dump(), subgoal_id=sub_goal_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(
    db: Session, db_task: models.Task, task_in: schemas.TaskUpdate
) -> models.Task:
    """
    Update an existing task.
    """
    update_data = task_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: UUID) -> models.Task | None:
    """
    Delete a task from the database by its ID.
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task
