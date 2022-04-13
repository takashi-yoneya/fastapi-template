from typing import List, Optional
import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import crud
import models
import schemas
from core.database import get_db
from core.logger import get_logger
from exceptions.core import APIException
from exceptions.error_messages import ErrorMessage
from schemas.core import PagingQueryIn

logger = get_logger(__name__)

router = APIRouter()


@router.get("/error")
def exec_error():
    # time.sleep(100)
    raise APIException(ErrorMessage.NOT_FOUND("デバックテストID"))

@router.get("/error2")
def exec_error2():
    # time.sleep(100)
    raise APIException(ErrorMessage.INTERNAL_SERVER_ERROR)

