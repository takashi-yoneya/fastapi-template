import datetime
from enum import Enum

from fastapi import Query

from app import schemas
from app.schemas.core import BaseSchema, PagingMeta
from app.schemas.tag import TagResponse


class TodoBase(BaseSchema):
    title: str | None = None
    description: str | None = None
    completed_at: datetime.datetime | None = None


class TodoResponse(TodoBase):
    id: str
    tags: list[TagResponse] | None = []
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
    # deleted_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True


class TodoCreate(TodoBase):
    title: str
    description: str | None = None


class TodoUpdate(TodoBase):
    pass


class TodosPagedResponse(BaseSchema):
    data: list[TodoResponse] | None = []
    meta: PagingMeta | None = None


class TodoSortFieldEnum(Enum):
    created_at = "created_at"
    title = "title"


class TodoSortQueryIn(schemas.SortQueryIn):
    sort_field: TodoSortFieldEnum | None = Query(TodoSortFieldEnum.created_at)
