from typing import Any, Optional

from httpx import Client
from starlette import status

from tests.testing_utils import assert_dict_part


class TestBase:
    ENDPOINT_URI: str = ...

    def assert_create(
        self,
        client: Client,
        data_in: dict,
        expected_status: int,
        expected_data: Optional[dict],
    ):
        res = client.post(self.ENDPOINT_URI, json=data_in)
        assert res.status_code == expected_status
        if expected_status == status.HTTP_200_OK:
            res_data = res.json()
            assert_dict_part(res_data, expected_data)

    def assert_update(
        self,
        client: Client,
        id: str,
        data_in: dict,
        expected_status: int,
        expected_data: Optional[dict],
    ):
        res = client.patch(f"{self.ENDPOINT_URI}/{id}", json=data_in)
        assert res.status_code == expected_status
        if expected_status == status.HTTP_200_OK:
            res_data = res.json()
            assert_dict_part(res_data, expected_data)

    def assert_get_by_id(
        self,
        client: Client,
        id: str,
        expected_status: int,
        expected_data: Optional[dict],
    ):
        res = client.get(f"{self.ENDPOINT_URI}/{id}")
        assert res.status_code == expected_status
        if expected_status == status.HTTP_200_OK:
            res_data = res.json()
            assert_dict_part(res_data, expected_data)

    def assert_get_paged_list(
        self,
        client: Client,
        params: dict[str, Any],
        expected_status: int,
        expected_first_data: dict,
        expected_paging_meta: dict,
    ):
        res = client.get(self.ENDPOINT_URI, params=params)
        assert res.status_code == expected_status
        if expected_status == status.HTTP_200_OK:
            res_data = res.json()
            assert res_data["data"]
            print(res_data["data"])
            assert_dict_part(res_data["data"][0], expected_first_data)
            assert_dict_part(res_data["meta"], expected_paging_meta)
