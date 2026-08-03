"""SQLAlchemy ORM models — the PMO domain, centred on projects.

  Project      a piece of work with dates, a budget, a RAG status and an owner.
  Milestone    a dated checkpoint within a project.
  Resource     a person, with a weekly capacity in hours.
  Allocation   how much of a resource is committed to a project (a % of capacity);
               one row per (resource, project) pair (enforced by a unique constraint).
  Risk         a project risk scored likelihood × impact, with a status and owner.

Milestones, risks and allocations are declared with cascade delete-orphan, so
removing a project (or a resource) also removes the records that hang off it and
leaves no orphans behind.
"""
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
from .enums import MilestoneStatus, ProjectCategory, RagStatus, RiskStatus


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String, default=ProjectCategory.OTHER.value)
    owner_resource_id: Mapped[int | None] = mapped_column(
        ForeignKey("resources.id"), nullable=True
    )
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    budget: Mapped[float | None] = mapped_column(Numeric(14, 2), nullable=True)
    actual_spend: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    rag_status: Mapped[str] = mapped_column(String, default=RagStatus.GREEN.value)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    owner: Mapped["Resource"] = relationship(
        "Resource", foreign_keys=[owner_resource_id]
    )
    milestones: Mapped[list["Milestone"]] = relationship(
        "Milestone", back_populates="project", cascade="all, delete-orphan"
    )
    risks: Mapped[list["Risk"]] = relationship(
        "Risk", back_populates="project", cascade="all, delete-orphan"
    )
    allocations: Mapped[list["Allocation"]] = relationship(
        "Allocation", back_populates="project", cascade="all, delete-orphan"
    )


class Milestone(Base):
    __tablename__ = "milestones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(
        String, default=MilestoneStatus.NOT_STARTED.value
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    project: Mapped["Project"] = relationship("Project", back_populates="milestones")


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    weekly_capacity_hours: Mapped[float] = mapped_column(Numeric(5, 2), default=40)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    allocations: Mapped[list["Allocation"]] = relationship(
        "Allocation", back_populates="resource", cascade="all, delete-orphan"
    )


class Allocation(Base):
    __tablename__ = "allocations"
    __table_args__ = (
        UniqueConstraint("resource_id", "project_id", name="uq_resource_project"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_id: Mapped[int] = mapped_column(
        ForeignKey("resources.id"), nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"), nullable=False
    )
    allocation_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    resource: Mapped["Resource"] = relationship(
        "Resource", back_populates="allocations"
    )
    project: Mapped["Project"] = relationship("Project", back_populates="allocations")


class Risk(Base):
    __tablename__ = "risks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    likelihood: Mapped[int] = mapped_column(Integer, nullable=False)
    impact: Mapped[int] = mapped_column(Integer, nullable=False)
    # score is stored (not derived on read) so the database can sort and filter on
    # it directly; it is kept equal to likelihood × impact when a risk is written.
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, default=RiskStatus.OPEN.value)
    mitigation_plan: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_resource_id: Mapped[int | None] = mapped_column(
        ForeignKey("resources.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    project: Mapped["Project"] = relationship("Project", back_populates="risks")
    owner: Mapped["Resource"] = relationship(
        "Resource", foreign_keys=[owner_resource_id]
    )
