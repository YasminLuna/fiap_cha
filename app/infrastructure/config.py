from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Oficina API"
    environment: str = "local"
    database_url: str = "sqlite:///./oficina.db"
    jwt_secret: str = "change-me"
    access_token_expire_minutes: int = 60
    admin_email: str = "admin@oficina.example.com"
    admin_password: str = "Admin123!"
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from: str = "no-reply@oficina.local"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
