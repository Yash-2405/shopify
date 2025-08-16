from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
from typing import Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Shopify Store Insights Fetcher"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "shopify_insights"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    
    # Web scraping settings
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 