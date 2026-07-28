from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas, serializers
from ..database import get_db

router = APIRouter(tags=["milestones"])


@router.get("/api/projects/{project_id}/milestones", response_model=list[schemas.MilestoneOut])
def list_milestones(project_id: int, db: Session = Depends(get_db)):
    if not crud.get_project(db, project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return [serializers.serialize_milestone(m) for m in crud.list_milestones_for_project(db, project_id)]


@router.post("/api/projects/{project_id}/milestones", response_model=schemas.MilestoneOut, status_code=201)
def create_milestone(project_id: int, data: schemas.MilestoneCreate, db: Session = Depends(get_db)):
    if not crud.get_project(db, project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return serializers.serialize_milestone(crud.create_milestone(db, project_id, data))


@router.put("/api/milestones/{milestone_id}", response_model=schemas.MilestoneOut)
def update_milestone(milestone_id: int, data: schemas.MilestoneUpdate, db: Session = Depends(get_db)):
    obj = crud.get_milestone(db, milestone_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return serializers.serialize_milestone(crud.update_milestone(db, obj, data))


@router.delete("/api/milestones/{milestone_id}", status_code=204)
def delete_milestone(milestone_id: int, db: Session = Depends(get_db)):
    obj = crud.get_milestone(db, milestone_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Milestone not found")
    crud.delete_milestone(db, obj)
