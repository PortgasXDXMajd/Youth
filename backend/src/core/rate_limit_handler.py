from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from starlette import status

from src.core.response import build_response


async def rate_limit_exceeded_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, RateLimitExceeded):
        status_code = status.HTTP_429_TOO_MANY_REQUESTS
        return JSONResponse(
            status_code=status_code,
            content=build_response(
                status=status_code,
                msg="Rate limit exceeded",
                data=None,
            ).model_dump(),
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=build_response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            msg="Internal server error",
            data=None,
        ).model_dump(),
    )
