from typing import List, Optional, Any
import time

import models
import schemas
from exceptions.core import APIException
from exceptions.error_messages import ErrorMessage
from .base import CRUDBase, Session, joinedload, Query, jsonable_encoder



class CRUDHashtag(
    CRUDBase[
        models.Job, 
        schemas.JobCreate, 
        schemas.JobUpdate,
        schemas.JobsPagedResponse
    ]
):
    pass
        
        
job = CRUDHashtag(
    models.Job, 
    schemas.JobsPagedResponse(data=[], meta=None)
)