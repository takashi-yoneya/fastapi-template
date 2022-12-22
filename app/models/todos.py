from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base

from . import ModelBase

todos_tags = Table(
    "todos_tags",
    Base.metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("todo_id", ForeignKey("todos.id"), index=True),
    Column("tag_id", ForeignKey("tags.id"), index=True),
    UniqueConstraint("todo_id", "tag_id", name="ix_todos_tags_todo_id_tag_id"),
)


class Todo(Base, ModelBase):

    __tablename__ = "todos"
    mysql_charset = ("utf8mb4",)
    mysql_collate = "utf8mb4_unicode_ci"

    title = Column(String(100), index=True)
    description = Column(Text)
    completed_at = Column(DateTime)

    tags = relationship("Tag", secondary=todos_tags, backref="todos")
