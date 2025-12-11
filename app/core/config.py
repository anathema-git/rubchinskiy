"""
Core configuration and settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "Fair Division System"
    debug: bool = False
    api_prefix: str = "/api"
    
    class Config:
        env_file = ".env"


settings = Settings()
