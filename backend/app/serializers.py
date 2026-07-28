"""Explicit ORM -> Pydantic conversion, including computed/enriched fields
(owner names, is_overdue, etc.) that don't exist directly as model columns.
"""
from datetime import date

from . import models, schemas
from .enums import MilestoneStatus


def serialize_resource(resource: models.Resource) -> schemas.ResourceOut:
    return schemas.ResourceOut(
        id=resource.id,
        name=resource.name,
        role=resource.role,
        email=resource.email,
        weekly_capacity_hours=float(resource.weekly_capacity_hours or 0),
        active=resource.active,
    )


def serialize_resource_detail(resource: models.Resource) -> schemas.ResourceDetailOut:
    base = serialize_resource(resource)
    return schemas.ResourceDetailOut(
        **base.model_dump(),
        allocations=[serialize_allocation(a) for a in resource.allocations],
    )


def serialize_allocation(allocation: models.Allocation) -> schemas.AllocationOut:
    return schemas.AllocationOut(
        id=allocation.id,
        resource_id=allocation.resource_id,
        project_id=allocation.project_id,
        allocation_pct=float(allocation.allocation_pct or 0),
        start_date=allocation.start_date,
        end_date=allocation.end_date,
        resource_name=allocation.resource.name if allocation.resource else None,
        project_name=allocation.project.name if allocation.project else None,
    )


def serialize_milestone(milestone: models.Milestone) -> schemas.MilestoneOut:
    is_overdue = bool(
        milestone.due_date
        and milestone.due_date < date.today()
        and milestone.status != MilestoneStatus.COMPLETE.value
    )
    return schemas.MilestoneOut(
        id=milestone.id,
        project_id=milestone.project_id,
        name=milestone.name,
        due_date=milestone.due_date,
        status=milestone.status,
        sort_order=milestone.sort_order,
        notes=milestone.notes,
        is_overdue=is_overdue,
    )


def serialize_risk(risk: models.Risk) -> schemas.RiskOut:
    return schemas.RiskOut(
        id=risk.id,
        project_id=risk.project_id,
        title=risk.title,
        description=risk.description,
        likelihood=risk.likelihood,
        impact=risk.impact,
        score=risk.score,
        status=risk.status,
        mitigation_plan=risk.mitigation_plan,
        owner_resource_id=risk.owner_resource_id,
        created_at=risk.created_at,
        updated_at=risk.updated_at,
        project_name=risk.project.name if risk.project else None,
        owner_name=risk.owner.name if risk.owner else None,
    )


def serialize_project(project: models.Project) -> schemas.ProjectOut:
    return schemas.ProjectOut(
        id=project.id,
        name=project.name,
        code=project.code,
        category=project.category,
        owner_resource_id=project.owner_resource_id,
        start_date=project.start_date,
        end_date=project.end_date,
        budget=float(project.budget) if project.budget is not None else None,
        actual_spend=float(project.actual_spend or 0),
        rag_status=project.rag_status,
        description=project.description,
        created_at=project.created_at,
        updated_at=project.updated_at,
        owner_name=project.owner.name if project.owner else None,
    )


def serialize_project_detail(project: models.Project) -> schemas.ProjectDetailOut:
    base = serialize_project(project)
    return schemas.ProjectDetailOut(
        **base.model_dump(),
        milestones=[serialize_milestone(m) for m in project.milestones],
        risks=[serialize_risk(r) for r in project.risks],
        allocations=[serialize_allocation(a) for a in project.allocations],
    )
