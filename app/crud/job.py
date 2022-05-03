import models
import schemas

from .base import CRUDBase


class CRUDHashtag(CRUDBase[models.Job, schemas.JobCreate, schemas.JobUpdate, schemas.JobsPagedResponse]):
    pass


job = CRUDHashtag(models.Job, schemas.JobsPagedResponse(data=[], meta=None))
