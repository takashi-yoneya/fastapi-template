import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):

    TITLE: str = "バックエンドAPI"
    CORS_ORIGINS: list = [
        "localhost:8000",
        "127.0.0.1:8000",
    ]
    BASE_DIR_PATH: str = str(Path(__file__).parent.parent.absolute())
    DATABASE_URI: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str = "secret"
    LOGGER_CONFIG_PATH: str = "logger_config.yaml"
    SENTRY_SDK_DNS: str = ""

    TEST_USER_EMAIL: str = ""
    TEST_DATABASE_URI: str = ""
    TEST_SQL_DATA_PATH: str = os.path.join(BASE_DIR_PATH, "tests", "test_data", "dump.sql.gz")

    IS_DOCKER_UVICORN: bool = None
    DOCKER_DATABASE_URI: str = "mysql+mysqlconnector://docker:docker@db/docker"
            
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
