import datetime
from typing import Optional

from app.schemas.core import BaseSchema, PagingMeta


class TagBase(BaseSchema):
    name: Optional[str]


class TagResponse(TagBase):
    id: str
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class TagCreate(TagBase):
    name: str


class TagUpdate(TagBase):
    pass


class TagsPagedResponse(BaseSchema):
    data: Optional[list[TagResponse]]
    meta: Optional[PagingMeta]
