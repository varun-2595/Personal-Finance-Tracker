from pydantic import BaseSettings
from functools import lru_cache
import os
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
    APP_PREFIX: str
    PROJECT_NAME: str
    
    class Config:
        env_file = "dev.env"
        

@lru_cache()
def get_settings() -> Settings:
    return Settings()