from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import get_settings

settings = get_settings()

client: Any = None
db: Any = None


async def connect_db() -> None:
    global client, db
    client = AsyncIOMotorClient(settings.mongo_url)
    db = client[settings.mongo_db]
    await db.users.create_index("email", unique=True)


async def close_db() -> None:
    global client
    if client:
        client.close()


def get_db() -> Any:
    return db
