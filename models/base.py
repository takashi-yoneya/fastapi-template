from sqlalchemy import (
    Column, 
    String, 
    DateTime, 
    Float, 
    Integer, 
    Boolean,
    Text,
    func
)
from sqlalchemy.sql.functions import current_timestamp

from core.database import Base
from core.utils import get_ulid


class ModelBase():    
    id = Column(String(32), primary_key=True, default=get_ulid)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    deleted_at = Column(DateTime)
