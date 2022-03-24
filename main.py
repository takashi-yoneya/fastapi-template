import logging
from fastapi import FastAPI, Security
from starlette.middleware.cors import CORSMiddleware
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from api.endpoints import jobs, users, login
from exceptions.exception_handlers import http_exception_handler
from core.config import get_settings
from core.auth import get_current_user
from core.logger import init_gunicorn_uvicorn_logger
settings = get_settings()
init_gunicorn_uvicorn_logger(settings.LOGGER_CONFIG_PATH)

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)

app = FastAPI(
    title = settings.TITLE
) 

if settings.SENTRY_SDK_DNS:
    sentry_sdk.init(
        dsn=settings.SENTRY_SDK_DNS,
        integrations=[sentry_logging, SqlalchemyIntegration()]
    )
    
app.add_middleware(
    CORSMiddleware,
    allow_origins = [str(origin) for origin in settings.CORS_ORIGINS],
    allow_methods = ["*"],
    allow_headers = ["*"]
)
app.add_middleware(SentryAsgiMiddleware)

app.add_exception_handler(Exception, http_exception_handler)

app.include_router(login.router, tags=["ログイン"], prefix="/login")
app.include_router(jobs.router, tags=["Jobs(求人)"], prefix="/jobs")
app.include_router(users.router, tags=["Users(ユーザーアカウント)"], prefix="/users")
