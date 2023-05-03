import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    # NOTE: .envファイルや環境変数が同名の変数にセットされる
    TITLE: str = "FastAPI Sample"
    ENV: str = ""
    DEBUG: bool = False
    VERSION: str = "0.0.1"
    CORS_ORIGINS: list[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://localhost:3333",
    ]
    BASE_DIR_PATH: str = str(Path(__file__).parent.parent.absolute())
    ROOT_DIR_PATH: str = str(Path(__file__).parent.parent.parent.absolute())
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER_NAME: str
    DB_PASSWORD: str
    API_GATEWAY_STAGE_PATH: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str = "secret"
    LOGGER_CONFIG_PATH: str = os.path.join(BASE_DIR_PATH, "logger_config.yaml")
    SENTRY_SDK_DNS: str = ""
    MIGRATIONS_DIR_PATH: str = os.path.join(ROOT_DIR_PATH, "alembic")

    def get_database_url(self, is_async: bool = False) -> str:
        if is_async:
            return (
                "mysql+aiomysql://"
                f"{self.DB_USER_NAME}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}/{self.DB_NAME}?charset=utf8mb4"
            )
        else:
            return (
                "mysql://"
                f"{self.DB_USER_NAME}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}/{self.DB_NAME}?charset=utf8mb4"
            )

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
