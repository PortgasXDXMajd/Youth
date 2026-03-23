from datetime import datetime, timezone
from typing import Protocol

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.db.session import get_db
from src.packages.users.entity import UserEntity


class UserRepositoryProtocol(Protocol):
    async def get_by_email(self, email: str) -> UserEntity | None: ...
    async def create(self, *, email: str, hashed_password: str, provider: str = "password") -> UserEntity: ...
    async def upsert_google_user(self, *, email: str, google_id: str) -> UserEntity: ...


class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase = Depends(get_db)) -> None:  # type: ignore[type-arg]
        self.db = db

    async def get_by_email(self, email: str) -> UserEntity | None:
        doc = await self.db.users.find_one({"email": email})
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])
        return UserEntity(**doc)

    async def create(
        self,
        *,
        email: str,
        hashed_password: str,
        provider: str = "password",
    ) -> UserEntity:
        now = datetime.now(timezone.utc)
        user_doc = {
            "email": email,
            "hashed_password": hashed_password,
            "provider": provider,
            "created_at": now,
            "modified_at": now,
        }
        result = await self.db.users.insert_one(user_doc)
        user_doc["_id"] = str(result.inserted_id)
        return UserEntity(**user_doc)

    async def upsert_google_user(self, *, email: str, google_id: str) -> UserEntity:
        now = datetime.now(timezone.utc)
        doc = await self.db.users.find_one_and_update(
            {"email": email},
            {
                "$set": {
                    "provider": "google",
                    "google_id": google_id,
                    "modified_at": now,
                },
                "$setOnInsert": {
                    "email": email,
                    "created_at": now,
                },
            },
            upsert=True,
            return_document=True,
        )
        doc["_id"] = str(doc["_id"])
        return UserEntity(**doc)
