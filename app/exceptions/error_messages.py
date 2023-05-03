from typing import Any

from starlette import status


class BaseMessage:
    """メッセージクラスのベース."""

    text: str
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, param: Any | None = None) -> None:
        self.param = param

    def __str__(self) -> str:
        return self.__class__.__name__


class ErrorMessage:
    """エラーメッセージクラス.

    Notes
    -----
        BaseMessagを継承することで
        Class呼び出し時にClass名がエラーコードになり、.textでエラーメッセージも取得できるため
        エラーコードと、メッセージの管理が直感的に行える。

    """

    # 共通
    class INTERNAL_SERVER_ERROR(BaseMessage):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        text = "システムエラーが発生しました、管理者に問い合わせてください"

    class FAILURE_LOGIN(BaseMessage):
        text = "ログインが失敗しました"

    class NOT_FOUND(BaseMessage):
        text = "{}が見つかりません"

    class ID_NOT_FOUND(BaseMessage):
        status_code = status.HTTP_404_NOT_FOUND
        text = "このidは見つかりません"

    class PARAM_IS_NOT_SET(BaseMessage):
        text = "{}がセットされていません"

    class ALREADY_DELETED(BaseMessage):
        text = "既に削除済です"

    class SOFT_DELETE_NOT_SUPPORTED(BaseMessage):
        text = "論理削除には未対応です"

    class COLUMN_NOT_ALLOWED(BaseMessage):
        text = "このカラムは指定できません"

    # ユーザー
    class ALREADY_REGISTED_EMAIL(BaseMessage):
        text = "登録済のメールアドレスです"

    class INCORRECT_CURRENT_PASSWORD(BaseMessage):
        text = "現在のパスワードが間違っています"

    class INCORRECT_EMAIL_OR_PASSWORD(BaseMessage):
        status_code = status.HTTP_403_FORBIDDEN
        text = "メールアドレスまたはパスワードが正しくありません"

    class PERMISSION_ERROR(BaseMessage):
        text = "実行権限がありません"

    class CouldNotValidateCredentials(BaseMessage):
        status_code = status.HTTP_403_FORBIDDEN
        text = "認証エラー"
