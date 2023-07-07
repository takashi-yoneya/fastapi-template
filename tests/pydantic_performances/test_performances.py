import time
from datetime import datetime, timezone

import pytest
from pydantic import BaseModel


class Tag(BaseModel):
    id: int
    tag: str


class Data(BaseModel):
    name: str
    age: int
    address: str
    point: float
    tags: list[Tag]
    created_at: datetime
    updated_at: datetime


@pytest.mark.skip(reason="pydantic v2のパフォーマンス検証用のため、通常のテストでは使用しない")
def test_check_performances() -> None:
    """pydantic v2のパフォーマンス検証用"""
    start = time.time()
    for i in range(1000000):
        data = Data(
            name=f"John{i}",
            age=20,
            address="New York",
            point=1.23,
            tags=[
                Tag(id=1, tag="tag1"),
                Tag(id=2, tag="tag2"),
                Tag(id=3, tag="tag3"),
            ],
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )
        data.model_dump_json()

    print(f"Time taken: {time.time() - start}")
