from sqlalchemy import or_
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, contains_eager
from sqlalchemy.sql import select

from app import crud_v2, models, schemas

from .base import CRUDV2Base


class CRUDTodo(
    CRUDV2Base[
        models.Todo,
        schemas.TodoResponse,
        schemas.TodoCreate,
        schemas.TodoUpdate,
        schemas.TodosPagedResponse,
    ],
):
    async def get_paged_list(  # type: ignore[override]
        self,
        db: AsyncSession,
        paging_query_in: schemas.PagingQueryIn,
        q: str | None = None,
        sort_query_in: schemas.SortQueryIn | None = None,
        include_deleted: bool = False,
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
        return await super().get_paged_list(
            db,
            paging_query_in=paging_query_in,
            where_clause=where_clause,
            sort_query_in=sort_query_in,
            include_deleted=include_deleted,
        )

    def add_tags_to_todo(
        self,
        db: Session,
        todo: models.Todo,
        tags_in: list[schemas.TagCreate],
    ) -> models.Todo:
        tags = crud_v2.tag.upsert_tags(db, tags_in=tags_in)
        todos_tags_data = [{"todo_id": todo.id, "tag_id": tag.id} for tag in tags]

        # Tagを紐づけ
        stmt = insert(models.TodoTag).values(todos_tags_data)
        stmt = stmt.on_duplicate_key_update(tag_id=stmt.inserted.tag_id)
        db.execute(stmt)

        stmt = (
            select(models.Todo)
            .outerjoin(models.Todo.tags)
            .options(contains_eager(models.Todo.tags))
            .where(models.Todo.id == todo.id)
        )
        todo = db.execute(stmt).scalars().unique().first()

        return todo


todo = CRUDTodo(
    models.Todo,
    response_schema_class=schemas.TodoResponse,
    list_response_class=schemas.TodosPagedResponse,
)
