from typing import Generator

from core.config import settings
from core.logger import get_logger
from debug_toolbar.panels.sqlalchemy import SQLAlchemyPanel
from fastapi import Request, Response
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = get_logger(__name__)


Base = declarative_base()
try:
    # if settings.IS_DOCKER_UVICORN:
    engine = create_engine(
        settings.DOCKER_DATABASE_URI,
        connect_args={"auth_plugin": "mysql_native_password"},
        pool_pre_ping=True,
    )
    logger.info(engine)
    # else:
    # engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    import traceback

    traceback.print_exc()
    print(e)
    print("DB connection failed")

if settings.DEBUG:

    class SQLAlchemyPanel_(SQLAlchemyPanel):
        async def process_request(self, request: Request) -> Response:
            self.register(engine)
            try:
                return await super().process_request(request)
            finally:
                self.unregister(engine)


def get_db() -> Generator:
    """
    endpointからアクセス時に、Dependで呼び出しdbセッションを生成する
    エラーがなければ、commitする
    エラー時はrollbackし、いずれの場合も最終的にcloseする
    """
    db = None
    try:
        db = SessionLocal()
        yield db
        db.commit()
    except Exception:
        if db:
            db.rollback()
    finally:
        if db:
            db.close()


def drop_all_tables() -> None:
    logger.info("start: drop_all_tables")
    """
    全てのテーブルおよび型、Roleなどを削除して、初期状態に戻す（開発環境専用）
    """
    if settings.ENV != "local":
        # ローカル環境でしか動作させない
        logger.info("drop_all_table() is ENV local only.")
        return None

    metadata = MetaData()
    metadata.reflect(bind=engine)

    # 外部キーの制御を一時的に無効化
    engine.execute("SET FOREIGN_KEY_CHECKS = 0")

    # 全テーブルを削除
    for table in metadata.tables:
        engine.execute(f"DROP TABLE {table} CASCADE")

    # 外部キーの制御を有効化
    engine.execute("SET FOREIGN_KEY_CHECKS = 1")
    logger.info("end: drop_all_tables")
