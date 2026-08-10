from functools import lru_cache
from os import getenv

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = 'RankPilot API'
    api_v1_prefix: str = '/api/v1'
    environment: str = 'development'
    database_url: str = 'postgresql+psycopg://rankpilot:rankpilot_password@localhost:5432/rankpilot'
    redis_url: str = 'redis://localhost:6379/0'
    cors_origins: list[str] = Field(default_factory=lambda: ['http://localhost:5173', 'http://127.0.0.1:5173'])


@lru_cache
def get_settings() -> Settings:
    cors_origins_raw = getenv('CORS_ORIGINS', '')
    cors_origins = [origin.strip() for origin in cors_origins_raw.split(',') if origin.strip()]

    return Settings(
        app_name=getenv('APP_NAME', 'RankPilot API'),
        api_v1_prefix=getenv('API_V1_PREFIX', '/api/v1'),
        environment=getenv('ENVIRONMENT', 'development'),
        database_url=getenv('DATABASE_URL', 'postgresql+psycopg://rankpilot:rankpilot_password@localhost:5432/rankpilot'),
        redis_url=getenv('REDIS_URL', 'redis://localhost:6379/0'),
        cors_origins=cors_origins or ['http://localhost:5173', 'http://127.0.0.1:5173'],
    )