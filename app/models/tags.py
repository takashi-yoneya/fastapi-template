from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship

from app.models.base import Base, ModelBaseMixin


class Tag(ModelBaseMixin, Base):
    __tablename__ = "tags"
    mysql_charset = ("utf8mb4",)
    mysql_collate = "utf8mb4_unicode_ci"

    name: Mapped[str] = Column(String(100), unique=True, index=True)

    todos: Mapped[list] = relationship(
        "Todo",
        secondary="todos_tags",
        back_populates="tags",
        lazy="joined",
    )
