from typing import Any
from urllib.request import Request

from fastapi.responses import PlainTextResponse

from app.core.logger import get_logger

logger = get_logger(__name__)


async def http_exception_handler(request: Request, exc: Any) -> PlainTextResponse:  # noqa: ARG001
    """HTTPリクエストに起因したExceptionエラー発生時のフック処理."""
    logger.exception(str(exc))
    return PlainTextResponse("Server Error: " + str(exc), status_code=500)
