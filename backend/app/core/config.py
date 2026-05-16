from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    env: str = "local"
    log_level: str = "INFO"

    database_url: str = "postgresql+psycopg://notescoon:notescoon@localhost:5432/notescoon"
    secret_key: str = "dev-secret-change-me"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()

    if settings.env.lower() == "production" and settings.secret_key == "dev-secret-change-me":
        raise ValueError("SECRET_KEY must be set in production")

    return settings
