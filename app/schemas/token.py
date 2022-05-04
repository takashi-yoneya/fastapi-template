from typing import Optional

from schemas.core import BaseSchema


class Token(BaseSchema):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenPayload(BaseSchema):
    sub: Optional[str]
