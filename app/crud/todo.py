from sqlalchemy import or_
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
    ],
):
    def get_paged_list(  # type: ignore[override]
        self,
        db: Session,
        paging_query_in: schemas.PagingQueryIn,
        q: str | None = None,
        sort_query_in: schemas.SortQueryIn | None = None,
    ) -> schemas.TodosPagedResponse:
        where_clause = (
            [
                or_(
                    models.Todo.title.ilike(f"%{q}%"),
                    models.Todo.description.ilike(f"%{q}%"),
                ),
            ]
            if q
            else []
        )
        return super().get_paged_list(
            db,
            paging_query_in=paging_query_in,
            where_clause=where_clause,
            sort_query_in=sort_query_in,
        )

    def add_tags_to_todo(
        self,
        db: Session,
        todo: models.Todo,
        tags_in: list[schemas.TagCreate],
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


todo = CRUDTodo(
    models.Todo,
    response_schema_class=schemas.TodoResponse,
    list_response_class=schemas.TodosPagedResponse,
)
