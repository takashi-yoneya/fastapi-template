from typing import Any

from sqlalchemy import Column, DateTime, String, event, func, orm
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp

from app.core.logger import get_logger
from app.core.utils import get_ulid

logger = get_logger(__name__)


class ModelBase:
    id = Column(String(32), primary_key=True, default=get_ulid)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(
        DateTime,
        nullable=False,
        default=current_timestamp(),
        onupdate=func.utc_timestamp(),
    )
    deleted_at = Column(DateTime)


@event.listens_for(Session, "do_orm_execute")
def _add_filtering_deleted_at(execute_state: Any) -> None:
    """
    論理削除用のfilterを自動的に適用する
    以下のようにすると、論理削除済のデータも含めて取得可能
    query(...).filter(...).execution_options(include_deleted=True)
    """
    logger.info(execute_state)
    if (
        execute_state.is_select
        and not execute_state.is_column_load
        and not execute_state.is_relationship_load
        and not execute_state.execution_options.get("include_deleted", False)
    ):
        execute_state.statement = execute_state.statement.options(
            orm.with_loader_criteria(  # ignore[mypy]
                ModelBase,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )

        logger.info(execute_state.statement)
