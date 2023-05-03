import logging

import sentry_sdk
from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI
from mangum import Mangum
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from starlette.middleware.cors import CORSMiddleware

from app.api.endpoints import auth, tasks, todos, users
from app.core.config import settings
from app.core.logger import get_logger

# loggingセットアップ

logger = get_logger(__name__)


class NoParsingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return not record.getMessage().find("/docs") >= 0


# /docsのログが大量に表示されるのを防ぐ
logging.getLogger("uvicorn.access").addFilter(NoParsingFilter())

sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)

app = FastAPI(
    title=f"[{settings.ENV}]{settings.TITLE}",
    version=settings.VERSION,
    debug=settings.DEBUG or False,
    root_path=f"{settings.API_GATEWAY_STAGE_PATH}/",
)


if settings.SENTRY_SDK_DNS:
    sentry_sdk.init(
        dsn=settings.SENTRY_SDK_DNS,
        integrations=[sentry_logging, SqlalchemyIntegration()],
        environment=settings.ENV,
    )


app.add_middleware(SentryAsgiMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_origin_regex=r"^https?:\/\/([\w\-\_]{1,}\.|)example\.com",
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/", tags=["info"])
def get_info() -> dict[str, str]:
    return {"title": settings.TITLE, "version": settings.VERSION}


app.include_router(auth.router, tags=["Auth"], prefix="/auth")
app.include_router(users.router, tags=["Users"], prefix="/users")
app.include_router(todos.router, tags=["Todos"], prefix="/todos")
app.include_router(tasks.router, tags=["Tasks"], prefix="/tasks")

if settings.DEBUG:
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
    )


handler = Mangum(app)
