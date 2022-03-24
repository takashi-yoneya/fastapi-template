from typing import List
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from core.database import get_db
from core.auth import get_current_user
from exceptions.core import APIException
from exceptions.error_messages import ErrorMessage
import models, schemas, crud


router = APIRouter()

@router.get("/me", response_model=schemas.UserResponse)
def get_user_me(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    return current_user

@router.get("/{id}", response_model=schemas.UserResponse, dependencies=[Security(get_current_user, scopes=["admin"])])
def get_user(
    id: str,
    db: Session = Depends(get_db)
):
    user = crud.user.get(db, id=id)
    if not user:
        raise APIException(ErrorMessage.ID_NOT_FOUND.make_error())
    return user

@router.post("/", response_model=schemas.UserResponse, dependencies=[Security(get_current_user, scopes=["admin"])])
def create_user(
    data_in: schemas.UserCreate,
    # current_user: models.User = Security(),
    db: Session = Depends(get_db),
):
    user = crud.user.get_by_email(db, email=data_in.email)
    if user:
        raise APIException(ErrorMessage.ALREADY_REGISTED_EMAIL.make_error())
    return crud.user.create(db, obj_in=data_in)

@router.put("/{id}", response_model=schemas.UserResponse, dependencies=[Security(get_current_user, scopes=["admin"])])
def update_user(
    id: str,
    data_in: schemas.UserUpdate,
    db: Session = Depends(get_db), 
):
    user = db.query(models.User).filter_by(id=id).first()
    if not user:
        raise APIException(ErrorMessage.ID_NOT_FOUND.make_error())
    return crud.user.update(db, db_obj=user, obj_in=data_in)


