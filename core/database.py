from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import get_settings

settings = get_settings()


Base = declarative_base()
try:
    if settings.IS_DOCKER_UVICORN:
        engine = create_engine(
            settings.DOCKER_DATABASE_URI, connect_args={"auth_plugin": "mysql_native_password"}, pool_pre_ping=True
        )
    else:
        engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    import traceback

    traceback.print_exc()
    print(e)
    print("DB connection failed")


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
    except:
        if db:
            db.rollback()
    finally:
        if db:
            db.close()
