from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserEntity(BaseModel):
    id: str = Field(alias="_id")
    email: EmailStr
    hashed_password: str | None = None
    provider: str = "password"
    google_id: str | None = None
    created_at: datetime
    modified_at: datetime

    model_config = {"populate_by_name": True}
