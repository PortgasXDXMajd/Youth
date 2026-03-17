from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    provider: str
    created_at: datetime
    modified_at: datetime
