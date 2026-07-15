from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name: str = "enterprise-ai-platform"
    environment: str = "development"
    log_level: str = "INFO"
    redis_url: str = "redis://localhost:6379"
    openai_api_key: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
@lru_cache
def get_settings() -> Settings:
    return Settings()
