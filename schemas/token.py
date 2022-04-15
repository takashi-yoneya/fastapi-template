from typing import List, Optional

from pydantic import BaseModel

from schemas.core import BaseSchema

class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenPayload(BaseSchema):
    sub: Optional[str]
