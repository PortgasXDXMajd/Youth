import asyncio
import os
from collections.abc import Iterator
from pathlib import Path
from unittest.mock import patch

import pytest
from mongomock_motor import AsyncMongoMockClient

os.environ["MONGO_URL"] = "mongodb://localhost:27017"
os.environ["MONGO_DB"] = "test_youth"
os.environ["JWT_SECRET_KEY"] = "test-secret-key"
os.environ["APP_ENV"] = "dev"
os.environ["GOOGLE_CLIENT_ID"] = "test-client-id"
os.environ["GOOGLE_CLIENT_SECRET"] = "test-client-secret"
os.environ["LOG_DIR"] = str(Path(__file__).resolve().parents[2] / "logs")

_mock_client = AsyncMongoMockClient()
_mock_db = _mock_client["test_youth"]


async def mock_connect_db(app_state: object) -> None:
    app_state.mongo_client = _mock_client  # type: ignore[attr-defined]
    app_state.db = _mock_db  # type: ignore[attr-defined]


async def mock_close_db(app_state: object) -> None:
    pass


with patch("src.db.session.connect_db", mock_connect_db), \
     patch("src.db.session.close_db", mock_close_db):
    from src.main import app  # noqa: E402

from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture(scope="session")
def client() -> Iterator[TestClient]:
    with patch("src.db.session.connect_db", mock_connect_db), \
         patch("src.db.session.close_db", mock_close_db):
        with TestClient(app) as test_client:
            yield test_client


@pytest.fixture(autouse=True)
def clean_db() -> None:
    async def _clean() -> None:
        await _mock_db.users.delete_many({})

    asyncio.run(_clean())
