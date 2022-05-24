from typing import List, Optional

from pydantic import EmailStr
from schemas.core import BaseSchema
from schemas.job import JobResponse


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
    jobs: Optional[List[JobResponse]]

    class Config:
        orm_mode = True
