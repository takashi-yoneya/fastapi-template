from sqlalchemy import Column, String, Text

from app.core.database import Base

from . import ModelBase


class Job(Base, ModelBase):

    __tablename__ = "jobs"
    mysql_charset = ("utf8mb4",)
    mysql_collate = "utf8mb4_unicode_ci"

    title = Column(String(100))
    description = Column(Text)
