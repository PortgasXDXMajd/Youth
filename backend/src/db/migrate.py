import asyncio
import importlib
import pkgutil
import sys
from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.core.config import get_settings

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def _load_modules() -> list[tuple[int, str]]:
    importlib.import_module("src.db.migrations")
    modules = sorted(
        pkgutil.iter_modules([str(MIGRATIONS_DIR)]),
        key=lambda m: m.name,
    )
    return [(int(m.name.split("_")[0]), m.name) for m in modules]


async def get_applied_versions(db: AsyncIOMotorDatabase) -> set[int]:
    cursor = db.migrations.find({}, {"version": 1})
    return {doc["version"] async for doc in cursor}


async def run_migrations(db: AsyncIOMotorDatabase) -> None:
    applied = await get_applied_versions(db)

    for version, name in _load_modules():
        if version in applied:
            continue

        module = importlib.import_module(f"src.db.migrations.{name}")
        print(f"Applying migration {name}...")
        await module.up(db)
        await db.migrations.insert_one({
            "version": version,
            "name": name,
        })
        print(f"Applied migration {name}")

    print("All migrations applied.")


async def rollback_migration(db: AsyncIOMotorDatabase, steps: int = 1) -> None:
    applied = await get_applied_versions(db)
    if not applied:
        print("Nothing to rollback.")
        return

    modules = [(v, n) for v, n in _load_modules() if v in applied]
    modules.sort(reverse=True)

    for version, name in modules[:steps]:
        module = importlib.import_module(f"src.db.migrations.{name}")
        print(f"Rolling back migration {name}...")
        await module.down(db)
        await db.migrations.delete_one({"version": version})
        print(f"Rolled back migration {name}")


async def main() -> None:
    settings = get_settings()
    client = AsyncIOMotorClient(settings.mongo_url)
    db = client[settings.mongo_db]
    try:
        command = sys.argv[1] if len(sys.argv) > 1 else "up"

        if command == "up":
            await run_migrations(db)
        elif command == "down":
            steps = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            await rollback_migration(db, steps)
        else:
            print(f"Unknown command: {command}. Use 'up' or 'down'.")
            sys.exit(1)
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())
