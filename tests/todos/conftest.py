from __future__ import annotations

import datetime

import pytest
from sqlalchemy.orm import Session

from app import models


@pytest.fixture
def data_set(db: Session):
    insert_todos(db)


def insert_todos(db: Session):
    now = datetime.datetime.now()
    data = [
        models.Todo(
            id=str(i),
            title=f"test-title-{i}",
            description=f"test-description-{i}",
            created_at=now - datetime.timedelta(days=i),
        )
        for i in range(1, 25)
    ]
    db.add_all(data)
    db.commit()
