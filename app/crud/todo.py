from sqlalchemy.orm import Session, contains_eager

from app import crud, models, schemas

from .base import CRUDBase


class CRUDTodo(CRUDBase[models.Todo, schemas.TodoCreate, schemas.TodoUpdate, schemas.TodosPagedResponse]):
    def add_tags_to_todo(self, db: Session, todo: models.Todo, tags_in: list[schemas.TagCreate]) -> models.Todo:
        tags = crud.tag.upsert_tags(db, tags_in=tags_in)
        for tag in tags:
            todo.tags.append(tag)
        db.flush()

        # one-to-many joined response one query
        todo = (
            db.query(models.Todo)
            .outerjoin(models.Todo.tags)
            .options(contains_eager(models.Todo.tags))
            .filter(models.Todo.id == todo.id)
            .first()
        )

        return todo


todo = CRUDTodo(models.Todo, schemas.TodosPagedResponse)
