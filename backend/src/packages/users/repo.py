from src.db.session import get_db


class UserRepository:
    def __init__(self) -> None:
        self.db = get_db()

    async def get_by_email(self, email: str) -> dict | None:
        return await self.db.users.find_one({"email": email})
