from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class GoogleAuthRequest(BaseModel):
    code: str
    redirect_uri: str


class TokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"
