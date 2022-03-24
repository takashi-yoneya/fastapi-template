from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from core.database import get_db
from exceptions.core import APIException
from exceptions.error_messages import ErrorMessage
import models
import schemas
import crud
from schemas.core import PagingQueryIn
from core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get("/{id}", response_model=schemas.JobResponse)
def get_job(
    id: str,
    db: Session = Depends(get_db)
):
    job = crud.job.get(db, id=id)
    if not job:
        raise APIException(ErrorMessage.ID_NOT_FOUND.make_error())
    return job


@router.get("/", response_model=schemas.JobsPagedResponse)
def get_jobs(
    q: Optional[str] = None,
    paging: PagingQueryIn = Depends(),
    # page: int = 1,
    # per_page: int = 30,
    db: Session = Depends(get_db)
):
    if q:
        query = db.query(models.Job).filter(models.Job.title.like(f"%{q}%"))
    else:
        query = db.query(models.Job)
    return crud.job.get_paged_list(db, paging=paging, filtered_query=query)


@router.post("/", response_model=schemas.JobResponse)
def create_job(
    data_in: schemas.JobCreate,
    db: Session = Depends(get_db)
):
    return crud.job.create(db, data_in)


@router.put("/{id}", response_model=schemas.JobResponse)
def update(
    id: str,
    data_in: schemas.JobUpdate,
    db: Session = Depends(get_db), 
):
    job = db.query(models.Job).filter_by(id=id).first()
    if not job:
        raise APIException(ErrorMessage.ID_NOT_FOUND.make_error())
    return crud.job.update(db, db_obj=job, obj_in=data_in)


@router.delete("/{id}", response_model=schemas.JobResponse)
def delete(
    id: str,
    db: Session = Depends(get_db), 
):
    job = db.query(models.Job).filter_by(id=id).first()
    if not job:
        raise APIException(ErrorMessage.ID_NOT_FOUND.make_error())
    return crud.job.delete(db, db_obj=job)