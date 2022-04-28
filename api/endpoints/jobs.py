from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy_filters import apply_filters, apply_sort

import crud
import models
import schemas
from core.database import get_db
from core.logger import get_logger
from exceptions.core import APIException
from exceptions.error_messages import ErrorMessage
from schemas.core import FilterQueryIn, PagingQueryIn

logger = get_logger(__name__)

router = APIRouter()


@router.get("/{id}", response_model=schemas.JobResponse)
def get_job(id: str, db: Session = Depends(get_db)):
    job = crud.job.get(db, id=id)
    if not job:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    return job


@router.get("", response_model=schemas.JobsPagedResponse)
def get_jobs(
    q: Optional[str] = None,
    paging: PagingQueryIn = Depends(),
    filter_params: FilterQueryIn = Depends(),
    db: Session = Depends(get_db),
):
    ALLOWED_COLUMNS = ["title", "created_at", "updated_at"]
    if not filter_params.validate_sort_column(ALLOWED_COLUMNS):
        raise APIException(ErrorMessage.COLUMN_NOT_ALLOWED)

    if q:
        query = db.query(models.Job).filter(models.Job.title.like(f"%{q}%"))
    else:
        query = db.query(models.Job)
    # if filter and filter.sort and (filter.start or filter.end):
    #     filter_dict = [
    #         {"model": "Job", "field": filter.sort, "op": ">=", "value": filter.start},
    #         {"model": "Job", "field": filter.sort, "op": "<=", "value": filter.end}
    #     ]
    #     query = apply_filters(query, filter_dict, do_auto_join=False)
    # if filter and filter.sort:
    #     sort_dict = [{
    #         "model": "Job", "field": filter.sort, "direction": filter.direction
    #     }]w
    #     query = apply_sort(query, sort_dict)

    return crud.job.get_paged_list(db, paging=paging, filtered_query=query, filter_params=filter_params)


@router.post("", response_model=schemas.JobResponse)
def create_job(data_in: schemas.JobCreate, db: Session = Depends(get_db)):
    return crud.job.create(db, data_in)


@router.put("/{id}", response_model=schemas.JobResponse)
def update(
    id: str,
    data_in: schemas.JobUpdate,
    db: Session = Depends(get_db),
):
    job = db.query(models.Job).filter_by(id=id).first()
    if not job:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    return crud.job.update(db, db_obj=job, obj_in=data_in)


@router.delete("/{id}", response_model=schemas.JobResponse)
def delete(
    id: str,
    db: Session = Depends(get_db),
):
    job = db.query(models.Job).filter_by(id=id).first()
    if not job:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    return crud.job.delete(db, db_obj=job)
