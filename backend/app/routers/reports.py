"""Read-only reporting endpoints. Each project is rolled up into a status summary
(milestone progress, open/high risks, RAG) suitable for a status report or export,
so the numbers a stakeholder sees are computed one way, in one place.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, models, schemas, serializers
from ..database import get_db
from ..enums import MilestoneStatus, RiskStatus

router = APIRouter(prefix="/api/reports", tags=["reports"])


# Condense one project into the summary numbers a status report needs: milestone
# counts by state, risk counts (open / high-severity), and the headline RAG.
def _project_rollup(project: models.Project) -> dict:
    milestones = project.milestones
    complete = sum(1 for m in milestones if m.status == MilestoneStatus.COMPLETE.value)
    pct_complete = (complete / len(milestones) * 100) if milestones else 0.0

    open_risks = [r for r in project.risks if r.status != RiskStatus.CLOSED.value]
    top_score = max((r.score for r in open_risks), default=0)

    return {
        "pct_milestones_complete": round(pct_complete, 1),
        "open_risk_count": len(open_risks),
        "top_risk_score": top_score,
    }


@router.get("/portfolio", response_model=list[schemas.PortfolioRow])
def portfolio_report(db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()
    rows = []
    for p in projects:
        rollup = _project_rollup(p)
        rows.append(
            schemas.PortfolioRow(
                project_id=p.id,
                name=p.name,
                code=p.code,
                category=p.category,
                rag_status=p.rag_status,
                owner_name=p.owner.name if p.owner else None,
                budget=float(p.budget) if p.budget is not None else None,
                actual_spend=float(p.actual_spend or 0),
                **rollup,
            )
        )
    return rows


@router.get("/project/{project_id}", response_model=schemas.ProjectReport)
def project_report(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    rollup = _project_rollup(project)
    return schemas.ProjectReport(
        project=serializers.serialize_project_detail(project),
        **rollup,
    )
