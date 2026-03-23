from fastapi import Depends
from starlette import status

from src.core.exceptions import AppException
from src.packages.users.model import UserRead
from src.packages.users.repo import UserRepository


class UserService:
    def __init__(self, repo: UserRepository = Depends()) -> None:
        self.repo = repo

    async def get_user_by_email(self, email: str) -> UserRead:
        user = await self.repo.get_by_email(email)
        if not user:
            raise AppException("User not found", status.HTTP_404_NOT_FOUND)
        return UserRead(
            email=user["email"],
            provider=user.get("provider", "password"),
            created_at=user["created_at"],
            modified_at=user["modified_at"],
        )
