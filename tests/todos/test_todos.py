from typing import Any, Optional

import pytest
from httpx import Client
from starlette import status

from app.schemas.core import PagingMeta
from app.schemas.todo import TodoCreate, TodoUpdate
from tests.base import TestBase

""" create """


class TestTodos(TestBase):
    ENDPOINT_URI = "/todos"

    """create
    """

    _params_create_todo = {
        "success": (
            TodoCreate(
                title="test-create-title", description="test-create-description"
            ).dict(by_alias=True),
            status.HTTP_200_OK,
            dict(title="test-create-title", description="test-create-description"),
            None,
        ),
    }

    @pytest.mark.parametrize(
        [
            "data_in",
            "expected_status",
            "expected_data",
            "expected_error",
        ],
        list(_params_create_todo.values()),
        ids=list(_params_create_todo.keys()),
    )
    def test_create(
        self,
        authed_client: Client,
        data_in: dict,
        expected_status: int,
        expected_data: Optional[dict],
        expected_error: Optional[dict],
    ) -> None:
        self.assert_create(
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
            dict(title="test-update-title", description="test-update-description"),
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
    def test_update(
        self,
        authed_client: Client,
        id: str,
        data_in: dict,
        expected_status: int,
        expected_data: Optional[dict],
        expected_error: Optional[dict],
        data_set: None,
    ) -> None:
        self.assert_update(
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
            dict(title="test-title-1", description="test-description-1"),
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
    def test_get_by_id(
        self,
        authed_client: Client,
        id: str,
        expected_status: int,
        expected_data: Optional[dict],
        expected_error: Optional[dict],
        data_set: None,
    ) -> None:
        self.assert_get_by_id(
            client=authed_client,
            id=id,
            expected_status=expected_status,
            expected_data=expected_data,
        )

    """get_paged_list
    """

    _params_get_paged_list = {
        "success": (
            dict(q="", perPage=10),
            status.HTTP_200_OK,
            dict(title="test-title-24", description="test-description-24"),
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
    def test_get_paged_list(
        self,
        authed_client: Client,
        params: dict[str, Any],
        expected_status: int,
        expected_first_data: Optional[dict],
        expected_paging_meta: dict,
        expected_error: Optional[dict],
        data_set: None,
    ) -> None:
        self.assert_get_paged_list(
            client=authed_client,
            params=params,
            expected_status=expected_status,
            expected_first_data=expected_first_data,
            expected_paging_meta=expected_paging_meta,
        )


# def test_get_user_report(
#     authed_client: Client,
#     base_data: None,
# ) -> None:
#     res = authed_client.get("/user_report/1")
#     assert res.status_code == status.HTTP_200_OK

#     res = authed_client.get("/user_report/100")
#     assert res.status_code == status.HTTP_400_BAD_REQUEST


# def test_get_paged_user_reports(
#     authed_client: Client,
#     base_data: None,
# ) -> None:
#     res = authed_client.get("/user_report")
#     assert res.status_code == status.HTTP_200_OK


# def test_delete_user_report(
#     authed_client: Client,
#     base_data: None,
# ) -> None:
#     res = authed_client.delete("/user_report/1")
#     assert res.status_code == status.HTTP_200_OK

#     res = authed_client.delete("/user_report/1")
#     assert res.status_code == status.HTTP_400_BAD_REQUEST


# params_update_user_report = {
#     "normal": (
#         "/user_report/1",
#         UserReportUpdate(status="inprogress").dict(),
#         status.HTTP_200_OK,
#     ),
#     "bad_request": (
#         "/user_report/100",
#         UserReportUpdate(status="inprogress").dict(),
#         status.HTTP_400_BAD_REQUEST,
#     ),
# }


# @pytest.mark.parametrize(
#     [
#         "url",
#         "data_in",
#         "expected_status",
#     ],
#     list(params_update_user_report.values()),
#     ids=list(params_update_user_report.keys()),
# )
# def test_update_user_report(
#     authed_client: Client,
#     base_data: None,
#     data_in: dict,
#     expected_status: int,
#     url: str,
# ) -> None:
#     res = authed_client.patch(url, json=data_in)
#     assert res.status_code == expected_status
