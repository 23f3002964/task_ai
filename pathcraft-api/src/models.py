import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Integer,
    Enum,
    JSON,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Goal(Base):
    __tablename__ = "goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, index=True)
    target_date = Column(DateTime(timezone=True), nullable=False)
    # As per the doc: SMART / OKR / custom
    methodology = Column(String, default="custom", nullable=False)

    # Relationship to SubGoal
    sub_goals = relationship(
        "SubGoal", back_populates="parent_goal", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Goal(title='{self.title}')>"


class SubGoal(Base):
    __tablename__ = "sub_goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_goal_id = Column(
        UUID(as_uuid=True), ForeignKey("goals.id"), nullable=False, index=True
    )
    description = Column(String, nullable=False)
    estimated_effort_minutes = Column(Integer, nullable=True)
    # Storing dependencies as a JSON array of SubGoal IDs for the MVP
    dependencies = Column(JSON, nullable=True)

    # Relationship to Goal
    parent_goal = relationship("Goal", back_populates="sub_goals")
    # Relationship to Task
    tasks = relationship(
        "Task", back_populates="sub_goal", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<SubGoal(description='{self.description}')>"


class TaskStatus(PyEnum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"
    SKIPPED = "skipped"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subgoal_id = Column(
        UUID(as_uuid=True), ForeignKey("sub_goals.id"), nullable=False, index=True
    )
    description = Column(String, nullable=False)  # Adding description for clarity
    planned_start = Column(DateTime(timezone=True), nullable=True)
    planned_end = Column(DateTime(timezone=True), nullable=True)
    actual_start = Column(DateTime(timezone=True), nullable=True)
    actual_end = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    # reminder_policy_id can be a FK to a future table. Storing as string for now.
    reminder_policy_id = Column(String, nullable=True)

    # Relationship to SubGoal
    sub_goal = relationship("SubGoal", back_populates="tasks")

    def __repr__(self):
        return f"<Task(description='{self.description}', status='{self.status.value}')>"
