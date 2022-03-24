import os
from pathlib import Path
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    
    TITLE: str = "バックエンドAPI"
    CORS_ORIGINS: list = [
        "localhost:8000",
        "127.0.0.1:8000",
    ]
    BASE_DIR_PATH: str = str(Path(__file__).parent.parent.absolute())
    print(BASE_DIR_PATH)
    DATABASE_URI: str = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str = "secret"    
    LOGGER_CONFIG_PATH: str = "logger_config.yaml"
    SENTRY_SDK_DNS = "https://86c412491f4b46df898a856752cc1a8a@o767328.ingest.sentry.io/6275120"
    
    TEST_USER_EMAIL: str = None
    TEST_DATABASE_URI: str = None
    TEST_SQL_DATA_PATH: str = os.path.join(BASE_DIR_PATH, "tests", "test_data", "dump.sql.gz") 
    
    
    class Config:
        env_file = ".env"
        
        
@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()