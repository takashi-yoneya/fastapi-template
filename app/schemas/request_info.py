from pydantic import ConfigDict

from app.schemas.core import BaseSchema


class RequestInfoResponse(BaseSchema):
    model_config = ConfigDict(from_attributes=True)
    ip_address: str | None
    host: str | None
