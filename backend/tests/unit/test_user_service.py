from datetime import datetime, timezone

import pytest

from src.core.exceptions import AppException
from src.packages.users.entity import UserEntity
from src.packages.users.service import UserService


class FakeUserRepo:
    def __init__(self, user: UserEntity | None) -> None:
        self.user = user

    async def get_by_email(self, email: str) -> UserEntity | None:
        return self.user

    async def create(self, *, email: str, hashed_password: str, provider: str = "password") -> UserEntity:
        raise NotImplementedError

    async def upsert_google_user(self, *, email: str, google_id: str) -> UserEntity:
        raise NotImplementedError


@pytest.mark.asyncio
async def test_get_user_by_email_not_found() -> None:
    service = UserService(repo=FakeUserRepo(user=None))

    with pytest.raises(AppException) as exc:
        await service.get_user_by_email("missing@example.com")

    assert exc.value.msg == "User not found"


@pytest.mark.asyncio
async def test_get_user_by_email_found() -> None:
    now = datetime.now(timezone.utc)
    user = UserEntity(
        _id="abc123",
        email="john@example.com",
        provider="password",
        created_at=now,
        modified_at=now,
    )
    service = UserService(repo=FakeUserRepo(user=user))

    result = await service.get_user_by_email("john@example.com")

    assert result.email == "john@example.com"
    assert result.provider == "password"
