from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core.database import get_db
from app.core.logger import get_logger
from app.exceptions.core import APIException
from app.exceptions.error_messages import ErrorMessage
from app.schemas.core import FilterQueryIn, PagingQueryIn

logger = get_logger(__name__)

router = APIRouter()


@router.get("/count")
def get_count(db: Session = Depends(get_db)) -> List[models.Job]:
    return db.query(func.count(models.Job.id)).all()


@router.get("/{id}", response_model=schemas.JobResponse, operation_id="get_job_by_id")
def get_job(
    id: str, include_deleted: bool = False, db: Session = Depends(get_db)
) -> models.Job:
    job = crud.job.get(db, id=id, include_deleted=include_deleted)
    if not job:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    return job


@router.get("", response_model=schemas.JobsPagedResponse, operation_id="get_jobs")
def get_jobs(
    q: Optional[str] = None,
    paging: PagingQueryIn = Depends(),
    filter_params: FilterQueryIn = Depends(),
    db: Session = Depends(get_db),
) -> schemas.JobsPagedResponse:
    ALLOWED_COLUMNS = ["title", "created_at", "updated_at"]
    if not filter_params.validate_allowed_sort_column(ALLOWED_COLUMNS):
        raise APIException(ErrorMessage.COLUMN_NOT_ALLOWED)

    if q:
        query = db.query(models.Job).filter(models.Job.title.like(f"%{q}%"))
    else:
        query = db.query(models.Job)

    return crud.job.get_paged_list(db, paging=paging, filtered_query=query)


@router.post("", response_model=schemas.JobResponse, operation_id="create_job")
def create_job(data_in: schemas.JobCreate, db: Session = Depends(get_db)) -> models.Job:
    return crud.job.create(db, data_in)


@router.patch("/{id}", response_model=schemas.JobResponse, operation_id="update_job")
def update_job(
    id: str,
    data_in: schemas.JobUpdate,
    db: Session = Depends(get_db),
) -> models.Job:
    job = db.query(models.Job).filter_by(id=id).first()
    if not job:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    return crud.job.update(db, db_obj=job, obj_in=data_in)


@router.delete("/{id}", response_model=schemas.JobResponse, operation_id="delete_job")
def delete_job(
    id: str,
    db: Session = Depends(get_db),
) -> models.Job:
    job = db.query(models.Job).filter_by(id=id).first()
    if not job:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    return crud.job.delete(db, db_obj=job)
