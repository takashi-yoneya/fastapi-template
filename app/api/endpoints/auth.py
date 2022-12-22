import datetime

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core import auth
from app.core.config import settings
from app.core.database import get_db
from app.exceptions.core import APIException
from app.exceptions.error_messages import ErrorMessage

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> schemas.Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise APIException(ErrorMessage.FAILURE_LOGIN)
    # elif not crud.user.is_active(user):
    #     raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(user.id, expires_delta=access_token_expires)
    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
    )
