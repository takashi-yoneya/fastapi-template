from pydantic import ConfigDict

from app.schemas.core import BaseSchema


class Token(BaseSchema):
    model_config = ConfigDict(alias_generator=None, populate_by_name=False, from_attributes=True)
    access_token: str
    token_type: str


class TokenPayload(BaseSchema):
    sub: str | None
