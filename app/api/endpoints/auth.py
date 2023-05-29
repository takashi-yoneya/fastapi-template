import datetime

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud_v2, schemas
from app.core import auth
from app.core.config import settings
from app.core.database import get_async_db
from app.exceptions.core import APIException
from app.exceptions.error_messages import ErrorMessage

router = APIRouter()


@router.post("/login")
async def login_access_token(
    db: AsyncSession = Depends(get_async_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> schemas.Token:
    """OAuth2 compatible token login, get an access token for future requests."""
    user = await crud_v2.user.authenticate(
        db,
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise APIException(ErrorMessage.FAILURE_LOGIN)

    access_token_expires = datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    access_token = auth.create_access_token(user.id, expires_delta=access_token_expires)
    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
    )
