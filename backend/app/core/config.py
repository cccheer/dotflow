from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "DotFlow Backend"
    api_prefix: str = "/api/v1"
    database_url: str = Field(
        default=f"sqlite:///{BASE_DIR / 'data' / 'dotflow.db'}",
        alias="DATABASE_URL",
    )
    admin_token: str = Field(default="change-me", alias="ADMIN_TOKEN")
    dot_api_base_url: str = Field(
        default="https://api.dot.dev",
        alias="DOT_API_BASE_URL",
    )
    dot_api_key: str = Field(default="", alias="DOT_API_KEY")
    dot_api_timeout_seconds: float = Field(default=10.0, alias="DOT_API_TIMEOUT_SECONDS")
    dot_api_mock: bool = Field(default=True, alias="DOT_API_MOCK")
    scheduler_timezone: str = Field(default="UTC", alias="SCHEDULER_TIMEZONE")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
