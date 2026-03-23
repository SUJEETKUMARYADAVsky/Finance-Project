from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Golf Charity Draw"
    environment: str = "development"
    secret_key: str = ""
    access_token_expire_minutes: int = 120
    database_url: str = "sqlite:///./golf_charity.db"
    cors_origins: str = "http://localhost:3000"
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    default_currency: str = "usd"
    allow_mock_payments: bool = True


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    if settings.environment != "development" and (not settings.secret_key or len(settings.secret_key) < 32):
        raise ValueError("SECRET_KEY must be set to a strong value in non-development environments")
    return settings
