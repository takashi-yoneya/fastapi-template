from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, ModelBaseMixin


class Todo(ModelBaseMixin, Base):
    __tablename__ = "todos"
    mysql_charset = ("utf8mb4",)
    mysql_collate = "utf8mb4_unicode_ci"

    title: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    tags: Mapped[list] = relationship(
        "Tag",
        secondary="todos_tags",
        back_populates="todos",
        lazy="joined",
    )
