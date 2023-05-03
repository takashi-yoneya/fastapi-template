from __future__ import annotations

import datetime

import pytest_asyncio
from app import models
from sqlalchemy.orm import Session


@pytest_asyncio.fixture
async def data_set(db: Session):
    await insert_todos(db)


async def insert_todos(db: Session):
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
    await db.commit()
