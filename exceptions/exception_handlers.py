import os
from urllib.request import Request

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from core.config import settings


async def http_exception_handler(request, exc):
    """
    HTTPリクエストに起因したExceptionエラー発生時のフック処理
    """

    return PlainTextResponse("Server Error: " + str(exc), status_code=500)
