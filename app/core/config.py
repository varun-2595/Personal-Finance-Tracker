from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
    
    # Authentication
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # Application
    DEBUG: bool
    API_PREFIX: str
    PROJECT_NAME: str
    
    model_config = SettingsConfigDict(
        env_file="dev.env",
        case_sensitive=True,
    )


@lru_cache()
def get_settings():
    return Settings()