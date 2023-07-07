from pydantic import ConfigDict, EmailStr

from app.schemas.core import BaseSchema, PagingMeta


class UserBase(BaseSchema):
    full_name: str | None = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: EmailStr
    email_verified: bool


class UsersPagedResponse(BaseSchema):
    data: list[UserResponse] | None
    meta: PagingMeta | None
