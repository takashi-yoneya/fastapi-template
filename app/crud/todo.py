from sqlalchemy.orm import Session, contains_eager

from app import crud, models, schemas

from .base import CRUDBase


class CRUDTodo(
    CRUDBase[
        models.Todo,
        schemas.TodoResponse,
        schemas.TodoCreate,
        schemas.TodoUpdate,
        schemas.TodosPagedResponse,
    ]
):
    def add_tags_to_todo(
        self, db: Session, todo: models.Todo, tags_in: list[schemas.TagCreate]
    ) -> models.Todo:
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

    # def get(self, db: Session, id: str, include_deleted: bool = False):
    #     schema_columns = list(schemas.TodoResponse.__fields__.keys())

    #     from sqlalchemy.inspection import inspect
    #     from sqlalchemy.orm.properties import ColumnProperty

    #     mapper = inspect(self.model)
    #     select_columns = [
    #         attr for attr in mapper.attrs if isinstance(attr, ColumnProperty) and attr.key in schema_columns
    #     ]
    #     return db.query(*select_columns).filter(models.Todo.id == id).first()


todo = CRUDTodo(
    models.Todo,
    response_schema_class=schemas.TodoResponse,
    list_response_class=schemas.TodosPagedResponse,
)
