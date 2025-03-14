from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Quote API Service"
    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    LOG_LEVEL: str = "INFO"

    # Database settings
    DATABASE_URL: str = "sqlite:///./quotes.db"

    # OpenTelemetry settings
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4317"
    OTEL_SERVICE_NAME: str = "quote_api_service"

    class Config:
        env_file = ".env"


settings = Settings() 