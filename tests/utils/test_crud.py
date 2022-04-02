import gzip

from sqlalchemy.orm import Session

from core.config import settings
from core.database import Base


def add_test_data(db: Session, objects: list):
    db.add_all(objects)
    db.commit()


def set_test_data(engine):
    with gzip.open(settings.TEST_SQL_DATA_PATH, mode="rt", encoding="utf-8") as fp:
        lines = ""
        for line in fp.readlines():
            line = line.strip()
            if not line:
                continue
            if line[0] == "/" or line[0] == "-":
                continue
            lines += line

        for sql in lines.split(";"):
            sql = sql.strip()
            if not sql:
                continue
            try:
                engine.execute(sql)
            except Exception as e:
                # logging.error(str(e))
                print(str(e))
                pass


def clear_and_set_test_data(engine):
    if settings.TEST_DATABASE_URI not in str(engine.url):
        raise Exception("test-db以外では実行できません")
    try:
        # 外部キーチェックを一時的に無効化
        engine.execute("SET FOREIGN_KEY_CHECKS = 0")

        # 既存データの削除
        for table_name in Base.metadata.tables:
            engine.execute(f"DROP TABLE {table_name}")

        # テーブルの作成
        Base.metadata.create_all(engine)

        # set_test_data(engine)

    except Exception as e:
        print("error", e)
    finally:
        engine.execute("SET FOREIGN_KEY_CHECKS = 1")
