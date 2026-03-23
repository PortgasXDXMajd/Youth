from fastapi import APIRouter, Depends, Request
from starlette import status

from src.core.rate_limit import limiter
from src.core.response import ResponseModel, build_response
from src.packages.auth.service import AuthService
from src.packages.users.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=ResponseModel,
    summary="Get current user",
    description="Returns authenticated user profile.",
)
@limiter.limit("30/minute")
async def get_me(
    request: Request,
    current_user_email: str = Depends(AuthService.get_current_user_email),
    service: UserService = Depends(),
) -> ResponseModel:
    user = await service.get_user_by_email(current_user_email)
    return build_response(status=status.HTTP_200_OK, msg="User fetched", data=user.model_dump())
