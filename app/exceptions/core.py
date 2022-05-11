from typing import Any, Dict, Optional

from fastapi import HTTPException, status


class APIException(HTTPException):
    """API例外"""

    default_status_code = status.HTTP_400_BAD_REQUEST

    def __init__(
        self,
        error: Any,
        status_code: int = default_status_code,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.status_code = status_code
        # self.detail =
        self.headers = headers

        # msg_paramsにセットしたパラメータをtextに展開する
        # try:
        #     error_code = error_obj
        #     error_obj.text
        #     message = error["error_code"].text.format(error["msg_param"])
        # except:
        #     message = error["error_code"].text
        try:
            error_obj = error()
        except Exception:
            error_obj = error

        try:
            message = error_obj.text.format(error_obj.param)
        except Exception:
            message = error_obj.text

        self.detail = {"error_code": str(error_obj), "error_msg": message}

        super().__init__(self.status_code, self.detail)
