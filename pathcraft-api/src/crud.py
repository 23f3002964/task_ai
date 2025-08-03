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

# You can add similar CRUD functions for SubGoal and Task here as needed.
# For now, we are focusing on the Goal entity.
