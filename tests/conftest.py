import logging
import os
from typing import Any, Generator

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mysql import factories
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

import alembic.command
import alembic.config
from app import schemas
from app.core.config import Settings
from app.core.database import get_db
from app.main import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


pytest.USER_ID = ""

logger.info("root-conftest")


class TestSettings(Settings):
    """テストのみで使用する設定を記述"""

    TEST_DB_HOST: str = "db"
    TEST_DB_USER: str = "root"
    TEST_DB_PORT: int = 3306
    # TEST_DB_PASSWORD: str = "pass"
    TEST_DB_NAME: str = "test"  # 一時的なテストDBを作成するので、アプリのDBとは別名にする

    TEST_USER_EMAIL: str = "test-user@example.com"
    TEST_USER_PASSWORD: str = "test-user"
    # TEST_SQL_DATA_PATH: str = os.path.join(BASE_DIR_PATH, "tests", "test_data", "dump.sql.gz")

    class Config:
        env_file = ".env.test"


settings = TestSettings()

logger.debug("start:mysql_proc")
db_proc = factories.mysql_noproc(
    host=settings.TEST_DB_HOST,
    port=settings.TEST_DB_PORT,
    user=settings.TEST_DB_USER,
)
mysql = factories.mysql("db_proc")
logger.debug("end:mysql_proc")


# TEST_USER_DICT = {
#     "email": settings.TEST_USER_EMAIL,
#     "password": settings.TEST_USER_PASSWORD,
#     "nickname": "test-user",
# }

TEST_USER_CREATE_SCHEMA = schemas.UserCreate(
    email=settings.TEST_USER_EMAIL,
    password=settings.TEST_USER_PASSWORD,
    full_name="test_user",
)


def migrate(
    versions_path: str,
    migrations_path: str,
    uri: str,
    alembic_ini_path: str,
    connection: Any = None,
    revision: str = "head",
) -> None:
    config = alembic.config.Config(alembic_ini_path)
    config.set_main_option("version_locations", versions_path)
    config.set_main_option("script_location", migrations_path)
    config.set_main_option("sqlalchemy.url", uri)
    # config.set_main_option("is_test", "1")
    if connection is not None:
        config.attributes["connection"] = connection
    alembic.command.upgrade(config, revision)


@pytest.fixture
def engine(
    mysql: Any,
):
    """fixture: db-engineの作成およびmigrate"""
    logger.debug("fixture:engine")
    uri = f"mysql://{settings.TEST_DB_USER}:@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}?charset=utf8mb4"
    settings.DATABASE_URI = uri
    engine = create_engine(uri, echo=False, poolclass=NullPool)

    with engine.begin() as conn:
        migrate(
            migrations_path=settings.MIGRATIONS_DIR_PATH,
            versions_path=os.path.join(settings.MIGRATIONS_DIR_PATH, "versions"),
            alembic_ini_path=os.path.join(settings.ROOT_DIR_PATH, "alembic.ini"),
            connection=conn,
            uri=uri,
        )
        logger.debug("migration end")

    return engine


@pytest.fixture
def db(
    engine,
) -> Generator[Session, None, None]:
    """fixture: db-sessionの作成"""
    logger.debug("fixture:db")
    test_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    with test_session_factory() as session:
        yield session
        session.commit()


@pytest.fixture
def client(engine) -> Generator[TestClient, None, None]:
    """fixture: HTTP-Clientの作成"""
    logger.debug("fixture:client")
    test_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db() -> Session:
        with test_session_factory() as session:
            yield session
            session.commit()

    # get_dbをTest用のDBを使用するようにoverrideする
    app.dependency_overrides[get_db] = override_get_db
    app.debug = False
    yield TestClient(app=app, base_url="http://test")


@pytest.fixture
def authed_client(client: TestClient) -> TestClient:
    # print(client.__dict__)
    """fixture: clietnに認証情報をセット"""
    logger.debug("fixture:authed_headers")
    res = client.post(
        "/users",
        json=TEST_USER_CREATE_SCHEMA.dict(),
    )
    assert res.status_code == status.HTTP_200_OK
    res = client.post(
        "/auth/login",
        data={
            "username": settings.TEST_USER_EMAIL,
            "password": settings.TEST_USER_PASSWORD,
        },
    )
    assert res.status_code == status.HTTP_200_OK
    access_token = res.json().get("access_token")
    client.headers = {"authorization": f"Bearer {access_token}"}

    # テスト全体で使用するので、グローバル変数とする
    res = client.get("users/me")
    assert res.json().get("id")
    pytest.USER_ID = res.json().get("id")

    return client


@pytest.fixture
def USER_ID(authed_client):
    return pytest.USER_ID
