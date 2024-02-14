import logging
from functools import lru_cache
from typing import Literal

from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Gitlab dumper settings."""

    GITLAB_URL: str
    GITLAB_OAUTH_TOKEN: str | None = None
    GITLAB_PERSONAL_TOKEN: str | None = None

    DEFAULT_DUMP_DIR: str = "./dumps"
    LOG_LEVEL: Literal["debug", "info", "warning", "error"] = "info"

    model_config: SettingsConfigDict = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    def __init__(self, *args, **kwargs):
        load_dotenv(find_dotenv())
        super().__init__(*args, **kwargs)


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_logger() -> logging.Logger:
    settings = get_settings()

    logging.basicConfig(
        level=settings.LOG_LEVEL.upper(),
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    return logging.getLogger("gitlab_dumper")


__all__ = ["get_settings", "get_logger", "Settings"]
