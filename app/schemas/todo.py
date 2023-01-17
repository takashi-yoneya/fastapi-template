import datetime
from enum import Enum
from typing import Optional

from fastapi import Query

from app import schemas
from app.schemas.core import BaseSchema, PagingMeta
from app.schemas.tag import TagResponse


class TodoBase(BaseSchema):
    title: Optional[str]
    description: Optional[str]
    completed_at: Optional[datetime.datetime]


class TodoResponse(TodoBase):
    id: str
    tags: Optional[list[TagResponse]]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    # deleted_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class TodoCreate(TodoBase):
    title: str
    description: Optional[str]


class TodoUpdate(TodoBase):
    pass


class TodosPagedResponse(BaseSchema):
    data: Optional[list[TodoResponse]]
    meta: Optional[PagingMeta]


class TodoSortFieldEnum(Enum):
    created_at = "created_at"
    title = "title"


class TodoSortQueryIn(schemas.SortQueryIn):
    sort_field: Optional[TodoSortFieldEnum] = Query(TodoSortFieldEnum.created_at)
