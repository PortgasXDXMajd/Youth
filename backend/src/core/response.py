from typing import Any

from pydantic import BaseModel


class ResponseModel(BaseModel):
    status: int
    msg: str
    data: Any | None = None


def build_response(status: int, msg: str, data: Any | None = None) -> ResponseModel:
    return ResponseModel(status=status, msg=msg, data=data)
