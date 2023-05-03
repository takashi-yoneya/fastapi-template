
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud_v2, schemas
from app.core.database import get_async_db
from app.core.logger import get_logger
from app.exceptions.core import APIException
from app.exceptions.error_messages import ErrorMessage
from app.schemas.core import PagingQueryIn

logger = get_logger(__name__)

router = APIRouter()


@router.get("/{id}", operation_id="get_todo_by_id")
async def get_job(
    id: str, include_deleted: bool = False, db: AsyncSession = Depends(get_async_db),
) -> schemas.TodoResponse:
    todo = await crud_v2.todo.get_db_obj_by_id(
        db, id=id, include_deleted=include_deleted,
    )
    print(todo)
    if not todo:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    return todo


@router.get("", operation_id="get_paged_todos")
async def get_paged_todos(
    q: str | None = None,
    paging_query_in: PagingQueryIn = Depends(),
    sort_query_in: schemas.TodoSortQueryIn = Depends(),
    include_deleted: bool = False,
    db: AsyncSession = Depends(get_async_db),
) -> schemas.TodosPagedResponse:
    return await crud_v2.todo.get_paged_list(
        db,
        q=q,
        paging_query_in=paging_query_in,
        sort_query_in=sort_query_in,
        include_deleted=include_deleted,
    )


@router.post("", operation_id="create_todo")
async def create_todo(
    data_in: schemas.TodoCreate, db: AsyncSession = Depends(get_async_db),
) -> schemas.TodoResponse:
    return await crud_v2.todo.create(db, data_in)


@router.patch("/{id}", operation_id="update_todo")
async def update_todo(
    id: str,
    data_in: schemas.TodoUpdate,
    db: AsyncSession = Depends(get_async_db),
) -> schemas.TodoResponse:
    todo = await crud_v2.todo.get_db_obj_by_id(db, id=id)
    if not todo:
        raise APIException(ErrorMessage.ID_NOT_FOUND)

    return await crud_v2.todo.update(db, db_obj=todo, update_schema=data_in)


@router.post("/{id}/tags", operation_id="add_tags_to_todo")
async def add_tags_to_todo(
    id: str,
    tags_in: list[schemas.TagCreate],
    db: AsyncSession = Depends(get_async_db),
) -> schemas.TodoResponse:
    todo = await crud_v2.todo.get_db_obj_by_id(db, id=id)
    if not todo:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    return await crud_v2.todo.add_tags_to_todo(db, todo=todo, tags_in=tags_in)


@router.delete(
    "/{id}", status_code=status.HTTP_204_NO_CONTENT, operation_id="delete_todo",
)
async def delete_todo(
    id: str,
    db: AsyncSession = Depends(get_async_db),
) -> None:
    todo = await crud_v2.todo.get_db_obj_by_id(db, id=id)
    if not todo:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    await crud_v2.todo.delete(db, db_obj=todo)
