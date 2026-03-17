from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "Youth API"
    app_env: str = Field(default="dev", pattern="^(dev|prod)$")
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_debug: bool = True

    mongo_url: str = "mongodb://localhost:27017"
    mongo_db: str = "YouthDb"

    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    google_client_id: str = ""
    google_client_secret: str = ""

    frontend_url: str = "http://localhost:3000"

    rate_limit_default: str = "100/minute"

    log_dir: str = str(BASE_DIR / "logs")
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env.dev"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


class ProdSettings(Settings):
    app_env: str = "prod"
    app_debug: bool = False
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env.prod"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    base = Settings()
    if base.app_env == "prod":
        return ProdSettings()
    return base
