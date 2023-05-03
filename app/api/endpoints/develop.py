from fastapi import APIRouter, Request

from app import schemas
from app.core import utils
from app.core.logger import get_logger
from app.exceptions.core import APIException
from app.exceptions.error_messages import ErrorMessage

logger = get_logger(__name__)

router = APIRouter()


@router.get("/error")
def exec_error() -> None:
    logger.error("debug test")
    print(1 / 0)
    raise APIException(ErrorMessage.NOT_FOUND("デバックテストID"))


@router.get("/error2")
def exec_error2() -> None:
    raise APIException(ErrorMessage.INTERNAL_SERVER_ERROR)


@router.get("/request-info")
def get_request_info(request: Request) -> schemas.RequestInfoResponse:
    ip_address = utils.get_request_info(request)
    host = utils.get_host_by_ip_address(ip_address)

    return schemas.RequestInfoResponse(ip_address=ip_address, host=host)
