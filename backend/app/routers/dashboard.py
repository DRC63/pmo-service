from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..enums import HIGH_SEVERITY_RISK_THRESHOLD, MilestoneStatus, RagStatus, RiskStatus

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=schemas.DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db)):
    today = date.today()
    horizon = today + timedelta(days=30)

    projects = db.query(models.Project).all()
    rag_counts = {status.value: 0 for status in RagStatus}
    for p in projects:
        rag_counts[p.rag_status] = rag_counts.get(p.rag_status, 0) + 1

    upcoming = (
        db.query(models.Milestone)
        .filter(
            models.Milestone.due_date.isnot(None),
            models.Milestone.due_date >= today,
            models.Milestone.due_date <= horizon,
            models.Milestone.status != MilestoneStatus.COMPLETE.value,
        )
        .order_by(models.Milestone.due_date)
        .limit(10)
        .all()
    )
    upcoming_milestones = [
        schemas.UpcomingMilestoneOut(
            project_id=m.project_id,
            project_name=m.project.name,
            milestone_id=m.id,
            name=m.name,
            due_date=m.due_date,
            days_until=(m.due_date - today).days if m.due_date else None,
        )
        for m in upcoming
    ]

    high_severity = (
        db.query(models.Risk)
        .filter(
            models.Risk.score >= HIGH_SEVERITY_RISK_THRESHOLD,
            models.Risk.status != RiskStatus.CLOSED.value,
        )
        .order_by(models.Risk.score.desc())
        .all()
    )
    high_severity_risks = [
        schemas.HighSeverityRiskOut(
            risk_id=r.id,
            project_id=r.project_id,
            project_name=r.project.name,
            title=r.title,
            score=r.score,
            status=r.status,
        )
        for r in high_severity
    ]

    overdue_count = (
        db.query(models.Milestone)
        .filter(
            models.Milestone.due_date.isnot(None),
            models.Milestone.due_date < today,
            models.Milestone.status != MilestoneStatus.COMPLETE.value,
        )
        .count()
    )

    return schemas.DashboardSummary(
        rag_counts=rag_counts,
        total_projects=len(projects),
        upcoming_milestones=upcoming_milestones,
        high_severity_risks=high_severity_risks,
        overdue_milestones_count=overdue_count,
    )
