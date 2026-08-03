"""HTTP endpoints for allocations — how much of a resource's capacity is committed
to a project. Because only one allocation may exist per (resource, project) pair,
a duplicate trips the database unique constraint (IntegrityError), which is caught
and returned as a clear 409 Conflict rather than a 500.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import crud, schemas, serializers
from ..database import get_db

router = APIRouter(prefix="/api/allocations", tags=["allocations"])


@router.get("", response_model=list[schemas.AllocationOut])
def list_allocations(
    resource_id: int | None = None,
    project_id: int | None = None,
    db: Session = Depends(get_db),
):
    allocations = crud.list_allocations(db, resource_id=resource_id, project_id=project_id)
    return [serializers.serialize_allocation(a) for a in allocations]


@router.post("", response_model=schemas.AllocationOut, status_code=201)
def create_allocation(data: schemas.AllocationCreate, db: Session = Depends(get_db)):
    if not crud.get_resource(db, data.resource_id):
        raise HTTPException(status_code=404, detail="Resource not found")
    if not crud.get_project(db, data.project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    try:
        return serializers.serialize_allocation(crud.create_allocation(db, data))
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="This resource is already allocated to this project. Edit the existing allocation instead.",
        )


@router.put("/{allocation_id}", response_model=schemas.AllocationOut)
def update_allocation(allocation_id: int, data: schemas.AllocationUpdate, db: Session = Depends(get_db)):
    obj = crud.get_allocation(db, allocation_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Allocation not found")
    return serializers.serialize_allocation(crud.update_allocation(db, obj, data))


@router.delete("/{allocation_id}", status_code=204)
def delete_allocation(allocation_id: int, db: Session = Depends(get_db)):
    obj = crud.get_allocation(db, allocation_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Allocation not found")
    crud.delete_allocation(db, obj)
