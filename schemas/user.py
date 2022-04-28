from typing import Optional

from pydantic import BaseModel, EmailStr

from schemas.core import BaseSchema


# Shared properties
class UserBase(BaseSchema):
    # email: Optional[EmailStr] = None
    full_name: Optional[str] = None


# Properties to receive via API on creation
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
