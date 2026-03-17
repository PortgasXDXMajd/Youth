from fastapi import APIRouter, Depends, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from starlette import status

from src.core.config import Settings, get_settings
from src.core.rate_limit import limiter
from src.core.response import ResponseModel, build_response
from src.db.session import get_db
from src.packages.auth.model import GoogleAuthRequest, LoginRequest, RegisterRequest
from src.packages.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=ResponseModel,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account using email and password.",
)
@limiter.limit("5/minute")
async def register(
    request: Request,
    payload: RegisterRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),  # type: ignore[type-arg]
    settings: Settings = Depends(get_settings),
) -> ResponseModel:
    user = await AuthService.register(payload, db, settings)
    return build_response(status=status.HTTP_201_CREATED, msg="User registered", data=user)


@router.post(
    "/login",
    response_model=ResponseModel,
    summary="Login user",
    description="Authenticate with email/password and return a JWT bearer token.",
)
@limiter.limit("10/minute")
async def login(
    request: Request,
    payload: LoginRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),  # type: ignore[type-arg]
    settings: Settings = Depends(get_settings),
) -> ResponseModel:
    token = await AuthService.login(payload, db, settings)
    return build_response(status=status.HTTP_200_OK, msg="Login successful", data=token.model_dump())


@router.post(
    "/google",
    response_model=ResponseModel,
    summary="Google OAuth login",
    description="Exchange Google authorization code for a JWT bearer token.",
)
@limiter.limit("10/minute")
async def google_auth(
    request: Request,
    payload: GoogleAuthRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),  # type: ignore[type-arg]
    settings: Settings = Depends(get_settings),
) -> ResponseModel:
    token = await AuthService.google_login(payload, db, settings)
    return build_response(status=status.HTTP_200_OK, msg="Login successful", data=token.model_dump())
