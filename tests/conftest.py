import logging
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient
from pydantic_settings import SettingsConfigDict
from pytest_mysql import factories
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import select

import alembic.command
import alembic.config
from app import schemas
from app.core.config import Settings
from app.core.database import get_async_db
from app.main import app
from app.models.base import Base
from app.models.users import User

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s %(levelname)s  %(message)s %(filename)s %(module)s %(funcName)s %(lineno)d",
)
logger = logging.getLogger(__name__)


pytest.USER_ID: str | None = None
pytest.USER_DICT: dict[str, Any] | None = None
pytest.ACCESS_TOKEN: str | None = None

logger.info("root-conftest")


class TestSettings(Settings):
    """テストのみで使用する設定を記述"""

    TEST_USER_EMAIL: str = "test-user1@example.com"
    TEST_USER_PASSWORD: str = "test-user"

    model_config = SettingsConfigDict(env_file=".env.test")


settings = TestSettings()

logger.debug("start:mysql_proc")
db_proc = factories.mysql_noproc(
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    user=settings.DB_USER_NAME,
)
mysql = factories.mysql("db_proc")
logger.debug("end:mysql_proc")


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


@pytest_asyncio.fixture
async def engine(
    mysql: Any,  # noqa: ARG001
) -> AsyncEngine:
    """fixture: db-engineの作成およびmigrate"""
    logger.debug("fixture:engine")
    # uri = (
    #     f"mysql+aiomysql://{settings.TEST_DB_USER}:"
    #     f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}?charset=utf8mb4"
    # )
    uri = settings.get_database_url(is_async=True)
    # sync_uri = (
    #     f"mysql://{settings.TEST_DB_USER}:"
    #     f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}?charset=utf8mb4"
    # )
    # settings.DATABASE_URI = uri
    engine = create_async_engine(uri, echo=False, poolclass=NullPool)

    # NOTE: テストケース毎にmigrateすると時間がかるので使用停止
    # migrate(alembic)はasyncに未対応なため、sync-engineを使用する
    # with sync_engine.begin() as conn:
    #     migrate(
    #         migrations_path=settings.MIGRATIONS_DIR_PATH,
    #         versions_path=os.path.join(settings.MIGRATIONS_DIR_PATH, "versions"),
    #         alembic_ini_path=os.path.join(settings.ROOT_DIR_PATH, "alembic.ini"),
    #         connection=conn,
    #         uri=sync_uri,
    #     )
    #     logger.debug("migration end")

    # create_allで一括処理する
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine


@pytest_asyncio.fixture
async def db(
    engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """fixture: db-sessionの作成"""
    logger.debug("fixture:db")
    test_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

    async with test_session_factory() as session:
        yield session
        await session.commit()


@pytest_asyncio.fixture
async def client(engine: AsyncEngine) -> AsyncClient:
    """fixture: HTTP-Clientの作成"""
    logger.debug("fixture:client")
    test_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with test_session_factory() as session:
            yield session
            await session.commit()

    # get_dbをTest用のDBを使用するようにoverrideする
    app.dependency_overrides[get_async_db] = override_get_db
    app.debug = False
    return AsyncClient(app=app, base_url="http://test")


async def _insert_user(db: AsyncSession, user_dict: dict[str, Any]) -> None:
    del user_dict["_sa_instance_state"]
    db.add(User(**user_dict))
    await db.commit()


@pytest_asyncio.fixture
async def authed_client(client: AsyncClient, db: AsyncSession) -> AsyncClient:
    """fixture: clietnに認証情報をセット"""
    logger.debug("fixture:authed_client")

    if pytest.USER_DICT:
        # すでに１度ユーザー登録している場合は、過去に登録したレコードを再登録する
        _insert_user(db, user_dict=pytest.USER_DICT)
        logger.debug("already user created. restore user.")
        client.headers = {"authorization": f"Bearer {pytest.ACCESS_TOKEN}"}
        return client

    # ユーザー登録
    res = await client.post(
        "/users",
        json=TEST_USER_CREATE_SCHEMA.dict(),
    )
    assert res.status_code == status.HTTP_200_OK

    # ログインしてアクセストークンを取得
    res = await client.post(
        "/auth/login",
        data={
            "username": settings.TEST_USER_EMAIL,
            "password": settings.TEST_USER_PASSWORD,
        },
    )
    assert res.status_code == status.HTTP_200_OK
    access_token = res.json().get("access_token")
    client.headers = {"authorization": f"Bearer {access_token}"}
    pytest.ACCESS_TOKEN = access_token

    # 登録したユーザーIDを取得
    res = await client.get("users/me")
    assert res.json().get("id")
    pytest.USER_ID = res.json().get("id")

    # ユーザーレコードを丸ごと取得して、次回以降のテストを高速化する
    stmt = select(User).where(User.id == res.json().get("id"))
    user = (await db.execute(stmt)).scalars().first()
    pytest.USER_DICT = user.__dict__.copy()

    return client


# @pytest.fixture
# def USER_ID(authed_client):
#     return pytest.USER_ID
