import time
from typing import Any, List, Optional

import models
import schemas
from exceptions.core import APIException
from exceptions.error_messages import ErrorMessage

from .base import CRUDBase, Query, Session, joinedload, jsonable_encoder


class CRUDHashtag(CRUDBase[models.Job, schemas.JobCreate, schemas.JobUpdate, schemas.JobsPagedResponse]):
    pass


job = CRUDHashtag(models.Job, schemas.JobsPagedResponse(data=[], meta=None))
