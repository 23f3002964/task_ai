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
    reminder_policy_id: Optional[str] = None


class TaskUpdate(BaseModel):
    description: Optional[str] = None
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    reminder_policy_id: Optional[str] = None


class Task(TaskBase):
    id: UUID
    subgoal_id: UUID
    status: TaskStatus
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    reminder_policy_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ====================
# SubGoal Schemas
# ====================


class SubGoalBase(BaseModel):
    description: str
    estimated_effort_minutes: Optional[int] = None
    dependencies: Optional[List[UUID]] = None
    notes: Optional[str] = None
    progress_percentage: int = 0


class SubGoalCreate(SubGoalBase):
    pass


class SubGoalUpdate(BaseModel):
    description: Optional[str] = None
    estimated_effort_minutes: Optional[int] = None
    dependencies: Optional[List[UUID]] = None
    notes: Optional[str] = None
    progress_percentage: Optional[int] = None


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
    notes: Optional[str] = None
    progress_percentage: int = 0


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    target_date: Optional[datetime] = None
    methodology: Optional[str] = None
    notes: Optional[str] = None
    progress_percentage: Optional[int] = None


class Goal(GoalBase):
    id: UUID
    sub_goals: List[SubGoal] = []

    model_config = ConfigDict(from_attributes=True)


# Pydantic v2 automatically handles forward references,
# so model_rebuild() is often not needed if types are annotated correctly.
# If issues arise, it can be called here:
# Goal.model_rebuild()
# SubGoal.model_rebuild()

# ====================
# ML Schemas
# ====================

class TimeSlot(BaseModel):
    start: datetime
    end: datetime

class ScheduleRequest(BaseModel):
    task_ids: List[UUID]
    available_slots: List[TimeSlot]

class OptimizedSlot(BaseModel):
    start: datetime
    end: datetime
    task_ids: List[UUID]

class Schedule(BaseModel):
    optimized_slots: List[OptimizedSlot]

class ReminderSuggestionRequest(BaseModel):
    user_id: str

class ReminderSuggestion(BaseModel):
    user_id: str
    suggestion: str

class ReminderReward(BaseModel):
    user_id: str
    arm: str
    reward: float
