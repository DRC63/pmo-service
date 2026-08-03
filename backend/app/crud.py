"""Database access helpers — the create/read/update/delete operations behind the
API routers, one small function per action.

Keeping the queries here rather than in the routers keeps the HTTP layer thin and
lets the same operations be reused and unit-tested without a request. Writes commit
immediately and refresh the object, so the caller gets server-set fields (id,
timestamps) back on the returned instance.
"""
from sqlalchemy.orm import Session

from . import models, schemas


# Risk score = likelihood × impact (each rated 1–5). Defined once here so the
# routers and the seed data all compute it the same way and the stored score stays
# consistent with the two inputs.
def compute_risk_score(likelihood: int, impact: int) -> int:
    return likelihood * impact


# ---------- Resource ----------
def list_resources(db: Session, active: bool | None = None):
    q = db.query(models.Resource)
    if active is not None:
        q = q.filter(models.Resource.active == active)
    return q.order_by(models.Resource.name).all()


def get_resource(db: Session, resource_id: int):
    return db.get(models.Resource, resource_id)


def create_resource(db: Session, data: schemas.ResourceCreate):
    obj = models.Resource(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_resource(db: Session, obj: models.Resource, data: schemas.ResourceUpdate):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_resource(db: Session, obj: models.Resource):
    db.delete(obj)
    db.commit()


# ---------- Project ----------
def list_projects(
    db: Session,
    category: str | None = None,
    rag_status: str | None = None,
    owner_id: int | None = None,
):
    q = db.query(models.Project)
    if category is not None:
        q = q.filter(models.Project.category == category)
    if rag_status is not None:
        q = q.filter(models.Project.rag_status == rag_status)
    if owner_id is not None:
        q = q.filter(models.Project.owner_resource_id == owner_id)
    return q.order_by(models.Project.name).all()


def get_project(db: Session, project_id: int):
    return db.get(models.Project, project_id)


def create_project(db: Session, data: schemas.ProjectCreate):
    obj = models.Project(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_project(db: Session, obj: models.Project, data: schemas.ProjectUpdate):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_project(db: Session, obj: models.Project):
    db.delete(obj)
    db.commit()


# ---------- Milestone ----------
def list_milestones_for_project(db: Session, project_id: int):
    return (
        db.query(models.Milestone)
        .filter(models.Milestone.project_id == project_id)
        .order_by(models.Milestone.sort_order, models.Milestone.due_date)
        .all()
    )


def get_milestone(db: Session, milestone_id: int):
    return db.get(models.Milestone, milestone_id)


def create_milestone(db: Session, project_id: int, data: schemas.MilestoneCreate):
    obj = models.Milestone(project_id=project_id, **data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_milestone(db: Session, obj: models.Milestone, data: schemas.MilestoneUpdate):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_milestone(db: Session, obj: models.Milestone):
    db.delete(obj)
    db.commit()


# ---------- Allocation ----------
def list_allocations(
    db: Session, resource_id: int | None = None, project_id: int | None = None
):
    q = db.query(models.Allocation)
    if resource_id is not None:
        q = q.filter(models.Allocation.resource_id == resource_id)
    if project_id is not None:
        q = q.filter(models.Allocation.project_id == project_id)
    return q.all()


def get_allocation(db: Session, allocation_id: int):
    return db.get(models.Allocation, allocation_id)


def create_allocation(db: Session, data: schemas.AllocationCreate):
    obj = models.Allocation(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_allocation(db: Session, obj: models.Allocation, data: schemas.AllocationUpdate):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_allocation(db: Session, obj: models.Allocation):
    db.delete(obj)
    db.commit()


# ---------- Risk ----------
def list_risks(
    db: Session,
    project_id: int | None = None,
    status: str | None = None,
    min_score: int | None = None,
):
    q = db.query(models.Risk)
    if project_id is not None:
        q = q.filter(models.Risk.project_id == project_id)
    if status is not None:
        q = q.filter(models.Risk.status == status)
    if min_score is not None:
        q = q.filter(models.Risk.score >= min_score)
    return q.order_by(models.Risk.score.desc()).all()


def get_risk(db: Session, risk_id: int):
    return db.get(models.Risk, risk_id)


def create_risk(db: Session, data: schemas.RiskCreate):
    payload = data.model_dump()
    payload["score"] = compute_risk_score(payload["likelihood"], payload["impact"])
    obj = models.Risk(**payload)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_risk(db: Session, obj: models.Risk, data: schemas.RiskUpdate):
    updates = data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(obj, key, value)
    if "likelihood" in updates or "impact" in updates:
        obj.score = compute_risk_score(obj.likelihood, obj.impact)
    db.commit()
    db.refresh(obj)
    return obj


def delete_risk(db: Session, obj: models.Risk):
    db.delete(obj)
    db.commit()
