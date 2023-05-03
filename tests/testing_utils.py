from typing import Any


def assert_dict_part(
    result_dict: dict[Any, Any],
    expected_dict: dict[Any, Any],
    exclude_fields: list[str] = [],
    expected_delete: bool = False,
) -> None:
    # 削除済データを取得する場合は、deleted_atにデータが存在することのみをチェックする
    if expected_delete:
        assert result_dict.get("deleted_at") or result_dict.get("deletedAt")
        exclude_fields.extend(["deleted_at", "deletedAt"])

    for key, value in expected_dict.items():
        if key in exclude_fields:
            continue
        assert (
            result_dict.get(key) == value
        ), f"key={key}. result_value={result_dict.get(key)}. expected_value={value}"


def assert_is_deleted(result_dict: dict[Any, Any]) -> None:
    assert result_dict.get("deleted_at")


def assert_successful_status_code(status_code: int) -> None:
    assert (
        300 > status_code >= 200
    ), f"status_code={status_code}. expected: 300 > status_code >= 200"


def assert_failed_status_code(status_code: int) -> None:
    assert not (
        300 > status_code >= 200
    ), f"status_code={status_code}. expected: not(300 > status_code >= 200)"


def assert_crud_model(
    result_obj: Any, expected_obj: Any, exclude_fileds: list[str] = []
) -> None:
    """
    sqlalchemy-modelのassertion
    """
    expected_dict = expected_obj.__dict__.copy()
    del expected_dict["_sa_instance_state"]
    for key, value in expected_dict.items():
        if key in exclude_fileds:
            continue
        assert (
            getattr(result_obj, key) == value
        ), f"{key=}, result_value={getattr(result_obj, key)}, expected_value={value}"


def assert_api_error(result_error: Any, expected_error: Any) -> None:
    assert result_error.detail["error_code"] == expected_error.detail["error_code"]
