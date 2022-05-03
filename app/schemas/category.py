from __future__ import annotations

import datetime
from typing import List, Optional

from schemas.core import BaseSchema, PagingMeta


class CategoryResponse(BaseSchema):
    id: str
    name: str
    deleted_at: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    parent_category: Optional[CategoryResponse]

    class Config:
        orm_mode = True


class CategoryCreate(BaseSchema):
    name: str
    parent_category_id: Optional[str] = None


class CategoryUpdate(BaseSchema):
    name: Optional[str] = None
    parent_category_id: Optional[str] = None


class CategoriesPagedResponse(BaseSchema):
    data: Optional[List[CategoryResponse]]
    meta: Optional[PagingMeta]
