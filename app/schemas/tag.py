import datetime

from pydantic import ConfigDict

from app.schemas.core import BaseSchema, PagingMeta


class TagBase(BaseSchema):
    name: str | None


class TagResponse(TagBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    deleted_at: datetime.datetime | None


class TagCreate(TagBase):
    name: str


class TagUpdate(TagBase):
    pass


class TagsPagedResponse(BaseSchema):
    data: list[TagResponse] | None
    meta: PagingMeta | None
