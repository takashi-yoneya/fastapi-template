from core.utils import get_ulid
from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql.functions import current_timestamp


class ModelBase:
    id = Column(String(32), primary_key=True, default=get_ulid)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    deleted_at = Column(DateTime)
