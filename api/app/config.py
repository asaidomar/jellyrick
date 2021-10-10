from functools import lru_cache
import os
from pydantic import BaseSettings

from .models.db_structure import Table


class Settings(BaseSettings):
    app_name: str = "JellyRick"
    secret_key_db_hash: str = os.getenv("DB_HASH_SECRET_KEY_DB")
    algorithm: str = os.getenv("DB_HASH_ALGORITHM")
    access_token_expire_minutes: str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    table = Table


@lru_cache()
def get_settings() -> Settings:
    return Settings()
