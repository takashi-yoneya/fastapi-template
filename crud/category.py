import time
from typing import Any, List, Optional

import models
import schemas
from exceptions.core import APIException
from exceptions.error_messages import ErrorMessage

from .base import CRUDBase, Query, Session, joinedload, jsonable_encoder


class CRUDCategory(
    CRUDBase[
        models.Category, 
        schemas.CategoryCreate, 
        schemas.CategoryUpdate, 
        schemas.CategoryResponse
    ]
):
    def updat_parent_category(self, db: Session, db_obj: models.Category, parent_category_id: str):
        db_obj.parent_category_id = parent_category_id
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj


category = CRUDCategory(
    models.Category, 
    schemas.CategoriesPagedResponse(data=[], meta=None)
)
