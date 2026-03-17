from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from src.core.response import build_response


class AppException(Exception):
    def __init__(
        self,
        msg: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        data: dict | None = None,
    ) -> None:
        self.msg = msg
        self.status_code = status_code
        self.data = data
        super().__init__(msg)


def _to_json(status_code: int, msg: str, data: dict | None = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=build_response(status=status_code, msg=msg, data=data).model_dump(),
    )


async def app_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, AppException):
        return _to_json(exc.status_code, exc.msg, exc.data)
    return _to_json(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")


async def http_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, HTTPException):
        return _to_json(exc.status_code, str(exc.detail))
    return _to_json(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")


async def validation_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, RequestValidationError):
        return _to_json(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Validation error",
            {"errors": exc.errors()},
        )
    return _to_json(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")


async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    return _to_json(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
