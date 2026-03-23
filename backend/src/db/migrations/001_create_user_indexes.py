from motor.motor_asyncio import AsyncIOMotorDatabase


async def up(db: AsyncIOMotorDatabase) -> None:
    await db.users.create_index("email", unique=True)


async def down(db: AsyncIOMotorDatabase) -> None:
    await db.users.drop_index("email_1")
