from typing import Any

import pytest
from app.schemas.core import PagingMeta
from app.schemas.todo import TodoCreate, TodoUpdate
from httpx import AsyncClient
from starlette import status

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

    _params_create_todo = {
        "success": (
            TodoCreate(
                title="test-create-title", description="test-create-description"
            ).dict(by_alias=True),
            status.HTTP_200_OK,
            {"title": "test-create-title", "description": "test-create-description"},
            None,
        ),
    }

    @pytest.mark.parametrize(
        ["data_in", "expected_status", "expected_data", "expected_error"],
        list(_params_create_todo.values()),
        ids=list(_params_create_todo.keys()),
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

    _params_update_todo = {
        "success": (
            "1",
            TodoUpdate(
                title="test-update-title", description="test-update-description"
            ).dict(by_alias=True),
            status.HTTP_200_OK,
            {"title": "test-update-title", "description": "test-update-description"},
            None,
        ),
        "error_id_not_found": (
            "not-found-id",
            TodoUpdate(
                title="test-update-title", description="test-update-description"
            ).dict(by_alias=True),
            status.HTTP_404_NOT_FOUND,
            None,
            None,
        ),
    }

    @pytest.mark.parametrize(
        [
            "id",
            "data_in",
            "expected_status",
            "expected_data",
            "expected_error",
        ],
        list(_params_update_todo.values()),
        ids=list(_params_update_todo.keys()),
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

    _params_get_todo_by_id = {
        "success": (
            "1",
            status.HTTP_200_OK,
            {"title": "test-title-1", "description": "test-description-1"},
            None,
        ),
        "error_id_not_found": (
            "not-found-id",
            status.HTTP_404_NOT_FOUND,
            None,
            None,
        ),
    }

    @pytest.mark.parametrize(
        [
            "id",
            "expected_status",
            "expected_data",
            "expected_error",
        ],
        list(_params_get_todo_by_id.values()),
        ids=list(_params_get_todo_by_id.keys()),
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

    _params_get_paged_list = {
        "success": (
            {"q": "", "perPage": 10},
            status.HTTP_200_OK,
            {"title": "test-title-24", "description": "test-description-24"},
            PagingMeta(
                current_page=1, total_page_count=3, total_data_count=24, per_page=10
            ).dict(by_alias=True),
            None,
        ),
    }

    @pytest.mark.parametrize(
        [
            "params",
            "expected_status",
            "expected_first_data",
            "expected_paging_meta",
            "expected_error",
        ],
        list(_params_get_paged_list.values()),
        ids=list(_params_get_paged_list.keys()),
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
