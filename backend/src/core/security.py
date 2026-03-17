from datetime import datetime, timedelta, timezone

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette import status

from src.core.config import Settings, get_settings
from src.core.exceptions import AppException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, settings: Settings, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.jwt_access_token_expire_minutes)
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str, settings: Settings) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise AppException(
            msg="Invalid or expired token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        ) from exc


def get_token_subject(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    settings: Settings = Depends(get_settings),
) -> str:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise AppException("Missing bearer token", status_code=status.HTTP_401_UNAUTHORIZED)

    payload = decode_token(credentials.credentials, settings)
    subject = payload.get("sub")
    if not subject:
        raise AppException("Invalid token payload", status_code=status.HTTP_401_UNAUTHORIZED)

    return str(subject)
