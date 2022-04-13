from __future__ import annotations
import datetime
from typing import List, Optional

from pydantic import BaseModel

from schemas.core import PagingMeta


class CategoryResponse(BaseModel):
    id: str
    name: str
    deleted_at: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    parent_category: Optional[CategoryResponse]

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    name: str
    parent_category_id: Optional[str] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_category_id: Optional[str] = None


class CategoriesPagedResponse(BaseModel):
    data: Optional[List[CategoryResponse]]
    meta: Optional[PagingMeta]
