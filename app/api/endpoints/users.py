from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from app import crud_v2, models, schemas
from app.core.auth import get_current_user
from app.core.database import get_async_db
from app.exceptions.core import APIException
from app.exceptions.error_messages import ErrorMessage

router = APIRouter()


@router.get("/me", response_model=schemas.UserResponse)
async def get_user_me(
    db: Session = Depends(get_async_db),
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    return current_user


@router.get(
    "/{id}",
    response_model=schemas.UserResponse,
    dependencies=[Security(get_current_user, scopes=["admin"])],
)
async def get_user(id: str, db: Session = Depends(get_async_db)) -> models.User:
    user = await crud_v2.user.get_db_obj_by_id(db, id=id)
    if not user:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    return user


@router.post("", response_model=schemas.UserResponse)
async def create_user(
    data_in: schemas.UserCreate,
    # current_user: models.User = Security(),
    db: Session = Depends(get_async_db),
) -> models.User:
    user = await crud_v2.user.get_by_email(db, email=data_in.email)
    if user:
        raise APIException(ErrorMessage.ALREADY_REGISTED_EMAIL)
    return await crud_v2.user.create(db, obj_in=data_in)


@router.put(
    "/{id}",
    response_model=schemas.UserResponse,
    dependencies=[Security(get_current_user, scopes=["admin"])],
)
async def update_user(
    id: str,
    data_in: schemas.UserUpdate,
    db: Session = Depends(get_async_db),
) -> models.User:
    user = await crud_v2.user.get_db_obj_by_id(db, id=id)
    if not user:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    return await crud_v2.user.update(db, db_obj=user, obj_in=data_in)
