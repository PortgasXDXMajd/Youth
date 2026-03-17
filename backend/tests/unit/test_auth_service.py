import pytest

from src.core.security import hash_password, verify_password, create_access_token, decode_token
from src.core.config import Settings


def test_hash_and_verify_password() -> None:
    password = "StrongPass123"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPass", hashed) is False


def test_create_and_decode_token() -> None:
    settings = Settings(jwt_secret_key="test-secret")
    token = create_access_token(subject="user@example.com", settings=settings)

    payload = decode_token(token, settings)

    assert payload["sub"] == "user@example.com"
    assert "exp" in payload
