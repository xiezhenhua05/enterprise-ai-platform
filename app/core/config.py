from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "enterprise-ai-platform"
    environment: str = "development"
    log_level: str = "INFO"
    redis_url: str = "redis://localhost:6379"
    openai_api_key: str = ""
    llm_api_key: str = ""
    llm_base_url: str = ""          # Base URL of the LLM service. Leave empty to use the official OpenAI endpoint;http://localhost:8001/v1 (local vLLM)
    llm_model: str = "gpt-4o-mini"  # Default model used for text generation. Examples:或 qwen2.5-7b-instruct 等
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    milvus_host: str = "localhost"
    milvus_port: int = 19530

@lru_cache
def get_settings() -> Settings:
    return Settings()
