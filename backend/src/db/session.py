from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import Request

from src.core.config import get_settings

settings = get_settings()


async def connect_db(app_state: object) -> None:
    client = AsyncIOMotorClient(settings.mongo_url)
    db = client[settings.mongo_db]
    await db.users.create_index("email", unique=True)
    app_state.mongo_client = client  # type: ignore[attr-defined]
    app_state.db = db  # type: ignore[attr-defined]


async def close_db(app_state: object) -> None:
    client = getattr(app_state, "mongo_client", None)
    if client:
        client.close()


def get_db(request: Request) -> AsyncIOMotorDatabase:
    return request.app.state.db
