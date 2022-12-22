from sqlalchemy import Column, String

from app.core.database import Base

from . import ModelBase


class Tag(Base, ModelBase):

    __tablename__ = "tags"
    mysql_charset = ("utf8mb4",)
    mysql_collate = "utf8mb4_unicode_ci"

    name = Column(String(100), unique=True, index=True)
