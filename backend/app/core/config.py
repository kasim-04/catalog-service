from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # пример: postgresql+psycopg2://user:pass@db:5432/cinema
    database_url: str = Field(default="postgresql+psycopg2://cinema:cinema@db:5432/cinema")

    # CORS для фронта (позже подправим под реальный домен/порт)
    cors_origins: str = Field(default="http://localhost:3000,http://localhost:5173")

    api_prefix: str = "/api"
    project_name: str = "Cinema Catalog Service"
    debug: bool = True

    # Простая "админка" без регистрации: токен из заголовка X-Admin-Token
    # Значение задавайте через переменную окружения ADMIN_TOKEN.
    admin_token: str = Field(default="change-me")


settings = Settings()
