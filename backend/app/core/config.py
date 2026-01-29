import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Property Management System"
    API_V1_STR: str = "/api/v1"
    
    # Database
    # Using SQLite for MVP ease of setup
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # AI Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    class Config:
        case_sensitive = True

settings = Settings()
