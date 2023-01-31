from typing import Optional

from pydantic import EmailStr

from app.schemas.core import BaseSchema, PagingMeta


class UserBase(BaseSchema):
    full_name: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserResponse(UserBase):
    id: str
    email: EmailStr
    email_verified: bool

    class Config:
        orm_mode = True


class UsersPagedResponse(BaseSchema):
    data: Optional[list[UserResponse]]
    meta: Optional[PagingMeta]
