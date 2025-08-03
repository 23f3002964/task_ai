from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from .models import TaskStatus

# ====================
# Task Schemas
# ====================

class TaskBase(BaseModel):
    description: str
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    description: Optional[str] = None
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    status: Optional[TaskStatus] = None

class Task(TaskBase):
    id: UUID
    subgoal_id: UUID
    status: TaskStatus
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

# ====================
# SubGoal Schemas
# ====================

class SubGoalBase(BaseModel):
    description: str
    estimated_effort_minutes: Optional[int] = None

class SubGoalCreate(SubGoalBase):
    pass

class SubGoalUpdate(BaseModel):
    description: Optional[str] = None
    estimated_effort_minutes: Optional[int] = None

class SubGoal(SubGoalBase):
    id: UUID
    parent_goal_id: UUID
    tasks: List[Task] = []

    model_config = ConfigDict(from_attributes=True)

# ====================
# Goal Schemas
# ====================

class GoalBase(BaseModel):
    title: str
    target_date: datetime
    methodology: str = "custom"

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    title: Optional[str] = None
    target_date: Optional[datetime] = None
    methodology: Optional[str] = None

class Goal(GoalBase):
    id: UUID
    sub_goals: List[SubGoal] = []

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

# Pydantic v2 automatically handles forward references,
# so model_rebuild() is often not needed if types are annotated correctly.
# If issues arise, it can be called here:
# Goal.model_rebuild()
# SubGoal.model_rebuild()
