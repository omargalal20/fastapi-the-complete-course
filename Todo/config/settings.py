import os
from functools import lru_cache

from pydantic_settings import BaseSettings


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    SQLITE_DATABASE_URL: str

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()
