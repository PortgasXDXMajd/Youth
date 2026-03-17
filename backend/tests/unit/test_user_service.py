from datetime import datetime, timezone

import pytest

from src.core.exceptions import AppException
from src.packages.users.service import UserService


class FakeUserRepo:
    def __init__(self, user: dict | None) -> None:
        self.user = user

    async def get_by_email(self, email: str) -> dict | None:
        return self.user


@pytest.mark.asyncio
async def test_get_user_by_email_not_found() -> None:
    service = UserService(repo=FakeUserRepo(user=None))

    with pytest.raises(AppException) as exc:
        await service.get_user_by_email("missing@example.com")

    assert exc.value.msg == "User not found"


@pytest.mark.asyncio
async def test_get_user_by_email_found() -> None:
    now = datetime.now(timezone.utc)
    user_doc = {
        "email": "john@example.com",
        "provider": "password",
        "is_active": True,
        "created_at": now,
        "modified_at": now,
    }
    service = UserService(repo=FakeUserRepo(user=user_doc))

    result = await service.get_user_by_email("john@example.com")

    assert result.email == "john@example.com"
    assert result.provider == "password"
    assert result.is_active is True
