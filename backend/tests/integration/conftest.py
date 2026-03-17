import asyncio
import os
from collections.abc import Iterator
from unittest.mock import patch

import pytest
from mongomock_motor import AsyncMongoMockClient

os.environ["MONGO_URL"] = "mongodb://localhost:27017"
os.environ["MONGO_DB"] = "test_youth"
os.environ["JWT_SECRET_KEY"] = "test-secret-key"
os.environ["APP_ENV"] = "dev"
os.environ["GOOGLE_CLIENT_ID"] = "test-client-id"
os.environ["GOOGLE_CLIENT_SECRET"] = "test-client-secret"

from src.db import session as db_session  # noqa: E402


async def mock_connect_db() -> None:
    db_session.client = AsyncMongoMockClient()
    db_session.db = db_session.client["test_youth"]
    await db_session.db.users.create_index("email", unique=True)


# Patch connect_db before importing the app so lifespan uses our mock
with patch("src.db.session.connect_db", mock_connect_db):
    from src.main import app  # noqa: E402

from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture(scope="session")
def client() -> Iterator[TestClient]:
    with patch("src.db.session.connect_db", mock_connect_db):
        with TestClient(app) as test_client:
            yield test_client


@pytest.fixture(autouse=True)
def clean_db() -> None:
    async def _clean() -> None:
        if db_session.db is not None:
            await db_session.db.users.delete_many({})

    asyncio.run(_clean())
