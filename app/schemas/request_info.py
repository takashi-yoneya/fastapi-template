
from app.schemas.core import BaseSchema


class RequestInfoResponse(BaseSchema):
    ip_address: str | None
    host: str | None

    class Config:
        orm_mode = True
