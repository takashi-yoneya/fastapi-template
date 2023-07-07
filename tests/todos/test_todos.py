from typing import Any

import pytest
from httpx import AsyncClient
from starlette import status

from app.schemas.core import PagingMeta
from app.schemas.todo import TodoCreate, TodoUpdate
from tests.base import (
    assert_create,
    assert_get_by_id,
    assert_get_paged_list,
    assert_update,
)


@pytest.mark.asyncio
class TestTodos:
    ENDPOINT_URI = "/todos"

    """create
    """

    @pytest.mark.parametrize(
        ["data_in", "expected_status", "expected_data", "expected_error"],
        [
            pytest.param(
                TodoCreate(title="test-create-title", description="test-create-description").model_dump(by_alias=True),
                status.HTTP_200_OK,
                {"title": "test-create-title", "description": "test-create-description"},
                None,
                id="success",
            )
        ],
    )
    async def test_create(
        self,
        authed_client: AsyncClient,
        data_in: dict,
        expected_status: int,
        expected_data: dict | None,
        expected_error: dict | None,
    ) -> None:
        await assert_create(
            self.ENDPOINT_URI,
            client=authed_client,
            data_in=data_in,
            expected_status=expected_status,
            expected_data=expected_data,
        )

    """update
    """

    @pytest.mark.parametrize(
        [
            "id",
            "data_in",
            "expected_status",
            "expected_data",
            "expected_error",
        ],
        [
            pytest.param(
                "1",
                TodoUpdate(title="test-update-title", description="test-update-description").dict(by_alias=True),
                status.HTTP_200_OK,
                {"title": "test-update-title", "description": "test-update-description"},
                None,
                id="success",
            ),
            pytest.param(
                "not-found-id",
                TodoUpdate(title="test-update-title", description="test-update-description").dict(by_alias=True),
                status.HTTP_404_NOT_FOUND,
                None,
                None,
                id="error_id_not_found",
            ),
        ],
    )
    async def test_update(
        self,
        authed_client: AsyncClient,
        id: str,
        data_in: dict,
        expected_status: int,
        expected_data: dict | None,
        expected_error: dict | None,
        data_set: None,
    ) -> None:
        await assert_update(
            self.ENDPOINT_URI,
            client=authed_client,
            id=id,
            data_in=data_in,
            expected_status=expected_status,
            expected_data=expected_data,
        )

    """get_by_id
    """

    @pytest.mark.parametrize(
        [
            "id",
            "expected_status",
            "expected_data",
            "expected_error",
        ],
        [
            pytest.param(
                "1",
                status.HTTP_200_OK,
                {"title": "test-title-1", "description": "test-description-1"},
                None,
                id="success",
            ),
            pytest.param(
                "not-found-id",
                status.HTTP_404_NOT_FOUND,
                None,
                None,
                id="error_id_not_found",
            ),
        ],
    )
    async def test_get_by_id(
        self,
        authed_client: AsyncClient,
        id: str,
        expected_status: int,
        expected_data: dict | None,
        expected_error: dict | None,
        data_set: None,
    ) -> None:
        await assert_get_by_id(
            self.ENDPOINT_URI,
            client=authed_client,
            id=id,
            expected_status=expected_status,
            expected_data=expected_data,
        )

    """get_paged_list
    """

    @pytest.mark.parametrize(
        [
            "params",
            "expected_status",
            "expected_first_data",
            "expected_paging_meta",
            "expected_error",
        ],
        [
            pytest.param(
                {"q": "", "perPage": 10},
                status.HTTP_200_OK,
                {"title": "test-title-24", "description": "test-description-24"},
                PagingMeta(current_page=1, total_page_count=3, total_data_count=24, per_page=10).dict(by_alias=True),
                None,
                id="success",
            )
        ],
    )
    async def test_get_paged_list(
        self,
        authed_client: AsyncClient,
        params: dict[str, Any],
        expected_status: int,
        expected_first_data: dict | None,
        expected_paging_meta: dict,
        expected_error: dict | None,
        data_set: None,
    ) -> None:
        await assert_get_paged_list(
            self.ENDPOINT_URI,
            client=authed_client,
            params=params,
            expected_status=expected_status,
            expected_first_data=expected_first_data,
            expected_paging_meta=expected_paging_meta,
        )
