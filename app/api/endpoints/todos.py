from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.database import get_db
from app.core.logger import get_logger
from app.exceptions.core import APIException
from app.exceptions.error_messages import ErrorMessage
from app.schemas.core import PagingQueryIn

logger = get_logger(__name__)

router = APIRouter()


@router.get("/{id}", response_model=schemas.TodoResponse, operation_id="get_todo_by_id")
def get_job(
    id: str, include_deleted: bool = False, db: Session = Depends(get_db)
) -> schemas.TodoResponse:
    todo = crud.todo.get_db_obj_by_id(db, id=id, include_deleted=include_deleted)
    if not todo:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    return todo


@router.get("", response_model=schemas.TodosPagedResponse, operation_id="get_todos")
def get_todos(
    q: Optional[str] = None,
    paging_query_in: PagingQueryIn = Depends(),
    sort_query_in: schemas.TodoSortQueryIn = Depends(),
    db: Session = Depends(get_db),
) -> schemas.TodosPagedResponse:
    return crud.todo.get_paged_list(
        db, q=q, paging_query_in=paging_query_in, sort_query_in=sort_query_in
    )


@router.post("", response_model=schemas.TodoResponse, operation_id="create_todo")
def create_todo(
    data_in: schemas.TodoCreate, db: Session = Depends(get_db)
) -> schemas.TodoResponse:
    try:
        return crud.todo.create(db, data_in)
    except Exception as e:
        logger.exception(e)


@router.patch("/{id}", response_model=schemas.TodoResponse, operation_id="update_todo")
def update_todo(
    id: str,
    data_in: schemas.TodoUpdate,
    db: Session = Depends(get_db),
) -> schemas.TodoResponse:
    todo = crud.todo.get_db_obj_by_id(db, id=id)
    if not todo:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    try:
        return crud.todo.update(db, db_obj=todo, update_schema=data_in)
    except Exception as e:
        logger.error(e)


@router.post(
    "/{id}/tags", response_model=schemas.TodoResponse, operation_id="add_tags_to_todo"
)
def add_tags_to_todo(
    id: str,
    tags_in: list[schemas.TagCreate],
    db: Session = Depends(get_db),
) -> schemas.TodoResponse:
    todo = crud.todo.get(db, id=id)
    if not todo:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    return crud.todo.add_tags_to_todo(db, todo=todo, tags_in=tags_in)
    # return crud.todo.update(db, db_obj=todo, obj_in=data_in)


@router.delete("/{id}", status_code=status.HTTP_200_OK, operation_id="delete_todo")
def delete_todo(
    id: str,
    db: Session = Depends(get_db),
) -> None:
    todo = crud.todo.get_db_obj_by_id(db, id=id)
    if not todo:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    crud.todo.delete(db, db_obj=todo)

    return None
