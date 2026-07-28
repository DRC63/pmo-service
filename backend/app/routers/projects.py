from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas, serializers
from ..database import get_db

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("", response_model=list[schemas.ProjectOut])
def list_projects(
    category: str | None = None,
    rag_status: str | None = None,
    owner_id: int | None = None,
    db: Session = Depends(get_db),
):
    projects = crud.list_projects(db, category=category, rag_status=rag_status, owner_id=owner_id)
    return [serializers.serialize_project(p) for p in projects]


@router.post("", response_model=schemas.ProjectOut, status_code=201)
def create_project(data: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return serializers.serialize_project(crud.create_project(db, data))


@router.get("/{project_id}", response_model=schemas.ProjectDetailOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    obj = crud.get_project(db, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project not found")
    return serializers.serialize_project_detail(obj)


@router.put("/{project_id}", response_model=schemas.ProjectOut)
def update_project(project_id: int, data: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    obj = crud.get_project(db, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project not found")
    return serializers.serialize_project(crud.update_project(db, obj, data))


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    obj = crud.get_project(db, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project not found")
    crud.delete_project(db, obj)
