from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import Request

from src.core.config import get_settings

settings = get_settings()


async def connect_db(app_state: object) -> None:
    client = AsyncIOMotorClient(
        settings.mongo_url,
        maxPoolSize=10,
        minPoolSize=1,
    )
    db = client[settings.mongo_db]
    app_state.mongo_client = client  # type: ignore[attr-defined]
    app_state.db = db  # type: ignore[attr-defined]


async def close_db(app_state: object) -> None:
    client = getattr(app_state, "mongo_client", None)
    if client:
        client.close()


async def get_db(request: Request) -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    yield request.app.state.db
