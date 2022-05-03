from typing import Any
from urllib.request import Request

from core.logger import get_logger
from fastapi.responses import PlainTextResponse

logger = get_logger(__name__)


async def http_exception_handler(request: Request, exc: Any) -> PlainTextResponse:
    """
    HTTPリクエストに起因したExceptionエラー発生時のフック処理
    """
    logger.error(str(exc))
    return PlainTextResponse("Server Error: " + str(exc), status_code=500)
