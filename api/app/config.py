from functools import lru_cache

from pydantic import BaseSettings

from app.models.db_model import Table


class Settings(BaseSettings):
    app_name: str = "JellyRick"
    table = Table


@lru_cache()
def get_settings() -> Settings:
    return Settings()
