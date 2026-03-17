from datetime import datetime, timezone
from typing import Any

from src.db.session import get_db


class AuthRepository:
    def __init__(self) -> None:
        self.db = get_db()

    async def get_user_by_email(self, email: str) -> dict | None:
        return await self.db.users.find_one({"email": email})

    async def create_user(
        self,
        *,
        email: str,
        hashed_password: str,
        provider: str = "password",
    ) -> dict:
        now = datetime.now(timezone.utc)
        user_doc = {
            "email": email,
            "hashed_password": hashed_password,
            "provider": provider,
            "is_active": True,
            "created_at": now,
            "modified_at": now,
        }
        result = await self.db.users.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id
        return user_doc

    async def upsert_google_user(self, *, email: str, google_id: str) -> dict:
        now = datetime.now(timezone.utc)
        result = await self.db.users.find_one_and_update(
            {"email": email},
            {
                "$set": {
                    "provider": "google",
                    "google_id": google_id,
                    "modified_at": now,
                },
                "$setOnInsert": {
                    "email": email,
                    "is_active": True,
                    "created_at": now,
                },
            },
            upsert=True,
            return_document=True,
        )
        return result
