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

    session_cookie_name: str = "notescoon_session"
    session_ttl_days: int = 7
    cookie_samesite: str = "lax"
    cookie_path: str = "/"

    @property
    def cookie_secure(self) -> bool:
        return self.env.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()

    db_url = settings.database_url.strip()
    if db_url.startswith("postgres://"):
        db_url = "postgresql://" + db_url[len("postgres://") :]
    if db_url.startswith("postgresql://"):
        db_url = "postgresql+psycopg://" + db_url[len("postgresql://") :]
    settings.database_url = db_url

    if settings.env.lower() == "production" and settings.secret_key == "dev-secret-change-me":
        raise ValueError("SECRET_KEY must be set in production")

    return settings
