import datetime
from typing import Optional

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
    deleted_at: Optional[datetime.datetime]

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
