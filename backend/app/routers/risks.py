from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas, serializers
from ..database import get_db

router = APIRouter(prefix="/api/risks", tags=["risks"])


@router.get("", response_model=list[schemas.RiskOut])
def list_risks(
    project_id: int | None = None,
    status: str | None = None,
    min_score: int | None = None,
    db: Session = Depends(get_db),
):
    risks = crud.list_risks(db, project_id=project_id, status=status, min_score=min_score)
    return [serializers.serialize_risk(r) for r in risks]


@router.post("", response_model=schemas.RiskOut, status_code=201)
def create_risk(data: schemas.RiskCreate, db: Session = Depends(get_db)):
    if not crud.get_project(db, data.project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return serializers.serialize_risk(crud.create_risk(db, data))


@router.get("/{risk_id}", response_model=schemas.RiskOut)
def get_risk(risk_id: int, db: Session = Depends(get_db)):
    obj = crud.get_risk(db, risk_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Risk not found")
    return serializers.serialize_risk(obj)


@router.put("/{risk_id}", response_model=schemas.RiskOut)
def update_risk(risk_id: int, data: schemas.RiskUpdate, db: Session = Depends(get_db)):
    obj = crud.get_risk(db, risk_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Risk not found")
    return serializers.serialize_risk(crud.update_risk(db, obj, data))


@router.delete("/{risk_id}", status_code=204)
def delete_risk(risk_id: int, db: Session = Depends(get_db)):
    obj = crud.get_risk(db, risk_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Risk not found")
    crud.delete_risk(db, obj)
