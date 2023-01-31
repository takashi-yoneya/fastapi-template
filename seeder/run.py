import logging
from pathlib import Path

import fire
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemyseed import Seeder, load_entities_from_json

from app.core import database
from app.core.config import settings
from app.core.logger.logger import init_logger

logger = logging.getLogger(__name__)


# TODO: できれば、Seederの処理と連動させたい
def truncate_tables(db: Session) -> None:
    TABLES = ["users"]

    db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

    for table in TABLES:
        db.execute(text(f"truncate {table}"))
        logger.info(f"truncate table={table}")

    db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))


def drop_all_tables() -> None:
    database.drop_all_tables()


def import_seed() -> None:
    logger.info("start: import_seed")
    seeds_json_files = list(Path(__file__).parent.glob("seeds_json/*.json"))
    db: Session = database.session_factory()
    try:
        truncate_tables(db)

        entities = []
        for file in seeds_json_files:
            logger.info(f"load seed file={str(file)}")
            entities.append(load_entities_from_json(str(file)))

        seeder = Seeder(db)
        seeder.seed(entities)
        db.commit()
        logger.info("end: seeds import completed")
    except Exception as e:
        db.rollback()
        logger.error(f"end: seeds import failed. detail={e}")


if __name__ == "__main__":
    init_logger(settings.LOGGER_CONFIG_PATH)
    fire.Fire()
