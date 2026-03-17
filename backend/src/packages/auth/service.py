import logging

import httpx
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from starlette import status

from src.core.config import Settings, get_settings
from src.core.exceptions import AppException
from src.core.security import (
    create_access_token,
    get_token_subject,
    hash_password,
    verify_password,
)
from src.db.session import get_db
from src.packages.auth.model import GoogleAuthRequest, LoginRequest, RegisterRequest, TokenData
from src.packages.users.repo import UserRepository

logger = logging.getLogger(__name__)

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


class AuthService:
    @staticmethod
    async def register(
        payload: RegisterRequest,
        db: AsyncIOMotorDatabase,  # type: ignore[type-arg]
        settings: Settings,
    ) -> dict:
        repo = UserRepository(db)
        existing = await repo.get_by_email(payload.email)
        if existing:
            raise AppException("Email already registered", status.HTTP_409_CONFLICT)

        user = await repo.create(
            email=payload.email,
            hashed_password=hash_password(payload.password),
        )
        logger.info("User registered email=%s", user["email"])
        return {
            "email": user["email"],
            "provider": user["provider"],
            "created_at": user["created_at"].isoformat(),
        }

    @staticmethod
    async def login(
        payload: LoginRequest,
        db: AsyncIOMotorDatabase,  # type: ignore[type-arg]
        settings: Settings,
    ) -> TokenData:
        repo = UserRepository(db)
        user = await repo.get_by_email(payload.email)
        if not user or "hashed_password" not in user:
            raise AppException("Invalid email or password", status.HTTP_401_UNAUTHORIZED)

        if not verify_password(payload.password, user["hashed_password"]):
            raise AppException("Invalid email or password", status.HTTP_401_UNAUTHORIZED)

        token = create_access_token(subject=user["email"], settings=settings)
        logger.info("User logged in email=%s", user["email"])
        return TokenData(access_token=token)

    @staticmethod
    async def google_login(
        payload: GoogleAuthRequest,
        db: AsyncIOMotorDatabase,  # type: ignore[type-arg]
        settings: Settings,
    ) -> TokenData:
        async with httpx.AsyncClient() as client:
            token_resp = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": payload.code,
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "redirect_uri": payload.redirect_uri,
                    "grant_type": "authorization_code",
                },
            )
            if token_resp.status_code != 200:
                raise AppException("Failed to exchange Google auth code", status.HTTP_400_BAD_REQUEST)

            access_token = token_resp.json()["access_token"]

            userinfo_resp = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if userinfo_resp.status_code != 200:
                raise AppException("Failed to get Google user info", status.HTTP_400_BAD_REQUEST)

        google_user = userinfo_resp.json()
        repo = UserRepository(db)
        user = await repo.upsert_google_user(
            email=google_user["email"],
            google_id=google_user["id"],
        )

        token = create_access_token(subject=user["email"], settings=settings)
        logger.info("Google login email=%s", user["email"])
        return TokenData(access_token=token)

    @staticmethod
    async def get_current_user_email(
        subject: str = Depends(get_token_subject),
        db: AsyncIOMotorDatabase = Depends(get_db),  # type: ignore[type-arg, assignment]
    ) -> str:
        repo = UserRepository(db)
        user = await repo.get_by_email(subject)
        if not user:
            raise AppException("User not found", status.HTTP_401_UNAUTHORIZED)
        return user["email"]
