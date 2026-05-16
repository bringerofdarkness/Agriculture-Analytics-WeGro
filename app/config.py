from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application settings loaded from environment variables.

    Local development uses .env.
    Production deployment should use platform secrets.
    """

    app_name: str = Field(default="Agriculture Analytics API")
    app_env: Literal["local", "development", "staging", "production"] = Field(
        default="local"
    )
    debug: bool = Field(default=False)

    mysql_host: str = Field(..., min_length=1)
    mysql_port: int = Field(default=3306, ge=1, le=65535)
    mysql_user: str = Field(..., min_length=1)
    mysql_password: SecretStr = Field(...)
    mysql_database: str = Field(default="agriculture_db", min_length=1)

    db_pool_size: int = Field(default=5, ge=1)
    db_max_overflow: int = Field(default=10, ge=0)
    db_pool_recycle_seconds: int = Field(default=1800, ge=300)
    db_echo: bool = Field(default=False)

    hf_port: int = Field(default=7860, ge=1, le=65535)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()