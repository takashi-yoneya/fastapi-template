from typing import Optional

from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


class CRUDJob(
    CRUDBase[
        models.Job,
        schemas.JobResponse,
        schemas.JobCreate,
        schemas.JobUpdate,
        schemas.JobsPagedResponse,
    ]
):
    SELECT_QUERY = [models.Job.id, models.Job.title, models.Job.updated_at]

    def get(
        self, db: Session, id: str, include_deleted: bool = False
    ) -> Optional[models.Job]:
        return super().get(db, id=id, include_deleted=include_deleted)


job = CRUDJob(
    models.Job,
    response_schema_class=schemas.JobResponse,
    list_response_class=schemas.JobsPagedResponse,
)
