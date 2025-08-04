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
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Goal(Base):
    __tablename__ = "goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    target_date = Column(DateTime(timezone=True), nullable=False)
    # As per the doc: SMART / OKR / custom
    methodology = Column(String, default="custom", nullable=False)
    notes = Column(String, nullable=True)

    # Relationship to SubGoal
    sub_goals = relationship(
        "SubGoal", back_populates="parent_goal", cascade="all, delete-orphan"
    )
    owner = relationship("User", back_populates="goals")

    # New field for progress tracking
    progress_percentage = Column(Integer, default=0, nullable=False)

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
    notes = Column(String, nullable=True)

    # Relationship to Goal
    parent_goal = relationship("Goal", back_populates="sub_goals")
    # Relationship to Task
    tasks = relationship(
        "Task", back_populates="sub_goal", cascade="all, delete-orphan"
    )

    # New field for progress tracking
    progress_percentage = Column(Integer, default=0, nullable=False)

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
    completed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    # reminder_policy_id can be a FK to a future table. Storing as string for now.
    reminder_policy_id = Column(String, nullable=True)

    # Relationship to SubGoal
    sub_goal = relationship("SubGoal", back_populates="tasks")

    def __repr__(self):
        return f"<Task(description='{self.description}', status='{self.status.value}')>"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    ab_test_group = Column(String, nullable=True)

    goals = relationship("Goal", back_populates="owner")

    def __repr__(self):
        return f"<User(username='{self.username}')>"


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    groups = Column(JSON, nullable=False)  # e.g., {"control": 0.5, "treatment": 0.5}
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Experiment(name='{self.name}')>"


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    value = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    experiment_id = Column(UUID(as_uuid=True), ForeignKey("experiments.id"), nullable=True, index=True)
    group = Column(String, nullable=True)

    def __repr__(self):
        return f"<Metric(name='{self.name}', value={self.value})>"


class Log(Base):
    __tablename__ = "logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    details = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<Log(event='{self.event}')>"
