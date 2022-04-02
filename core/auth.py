from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session

import crud
import models
import schemas
from exceptions.core import APIException
from exceptions.error_messages import ErrorMessage

from .config import settings
from .database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token", scopes={"admin": "Admin user only"})


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_current_user(
    security_scopes: SecurityScopes,
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> models.User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise APIException(
            status_code=status.HTTP_403_FORBIDDEN,
            error=ErrorMessage.CouldNotValidateCredentials.make_error(),
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise APIException(ErrorMessage.NOT_FOUND.make_error("User"))
    user_scopes = user.scopes.split(",") if user.scopes else []
    for scope in security_scopes.scopes:
        if scope not in user_scopes:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                error=ErrorMessage.PERMISSION_ERROR.make_error(),
            )
    return user


# def get_current_active_user(
#     current_user: models.User = Depends(get_current_user),
# ) -> models.User:
#     if not crud.user.is_active(current_user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# def get_current_active_superuser(
#     current_user: models.User = Depends(get_current_user),
# ) -> models.User:
#     if not crud.user.is_superuser(current_user):
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return
