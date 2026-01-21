import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise AI Agent"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    OPENAI_API_KEY: str
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:8501", "http://localhost:8000"]

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()
