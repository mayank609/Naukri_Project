from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Keys
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    starapi_key: str = os.getenv("STARAPI_KEY", "")
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./social_analytics.db")
    
    # App Configuration
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-this")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    allowed_hosts: str = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
    
    # Instagram Configuration
    instagram_username: Optional[str] = os.getenv("INSTAGRAM_USERNAME")
    instagram_password: Optional[str] = os.getenv("INSTAGRAM_PASSWORD")
    
    # Content Generation Settings
    max_tokens: int = int(os.getenv("MAX_TOKENS", "2000"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    class Config:
        env_file = ".env"

settings = Settings() 