"""HTTP endpoints for resources (people): list (optionally filtered to active),
get one with its allocations, and create/update/delete. Thin layer over crud +
serializers.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas, serializers
from ..database import get_db

router = APIRouter(prefix="/api/resources", tags=["resources"])


@router.get("", response_model=list[schemas.ResourceOut])
def list_resources(active: bool | None = None, db: Session = Depends(get_db)):
    return [serializers.serialize_resource(r) for r in crud.list_resources(db, active=active)]


@router.post("", response_model=schemas.ResourceOut, status_code=201)
def create_resource(data: schemas.ResourceCreate, db: Session = Depends(get_db)):
    return serializers.serialize_resource(crud.create_resource(db, data))


@router.get("/{resource_id}", response_model=schemas.ResourceDetailOut)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    obj = crud.get_resource(db, resource_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Resource not found")
    return serializers.serialize_resource_detail(obj)


@router.put("/{resource_id}", response_model=schemas.ResourceOut)
def update_resource(resource_id: int, data: schemas.ResourceUpdate, db: Session = Depends(get_db)):
    obj = crud.get_resource(db, resource_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Resource not found")
    return serializers.serialize_resource(crud.update_resource(db, obj, data))


@router.delete("/{resource_id}", status_code=204)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    obj = crud.get_resource(db, resource_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Resource not found")
    crud.delete_resource(db, obj)
