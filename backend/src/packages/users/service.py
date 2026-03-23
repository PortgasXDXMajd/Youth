from typing import Protocol

from fastapi import Depends
from starlette import status

from src.core.exceptions import AppException
from src.packages.users.model import UserRead
from src.packages.users.repo import UserRepository, UserRepositoryProtocol


class UserService:
    def __init__(self, repo: UserRepositoryProtocol = Depends(UserRepository)) -> None:
        self.repo = repo

    async def get_user_by_email(self, email: str) -> UserRead:
        user = await self.repo.get_by_email(email)
        if not user:
            raise AppException("User not found", status.HTTP_404_NOT_FOUND)
        return UserRead.model_validate(user)
