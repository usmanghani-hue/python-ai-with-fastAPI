"""
Central configuration for the whole application.

Every setting is loaded from environment variables (see .env.example).
Nothing in this file should ever contain a real secret — this defines
*where* config comes from, not the values themselves.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- App ---
    app_env: str = "development"
    app_secret_key: str
    log_level: str = "INFO"

    # --- Database ---
    database_url: str

    # --- Redis ---
    redis_url: str = "redis://localhost:6379/0"

    # --- LLM ---
    groq_api_key: str
    llm_model: str = "llama-3.3-70b-versatile"
    llm_max_tokens: int = 1024
    llm_temperature: float = 0.2

    # --- Embeddings ---
    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536

    # --- WhatsApp Cloud API ---
    whatsapp_phone_number_id: str
    whatsapp_business_account_id: str
    whatsapp_access_token: str
    whatsapp_app_secret: str
    whatsapp_webhook_verify_token: str
    whatsapp_api_version: str = "v20.0"

    # --- Admin auth ---
    admin_jwt_secret: str
    admin_jwt_expire_minutes: int = 120

    # --- RAG ---
    retrieval_top_k: int = 5
    retrieval_confidence_threshold: float = 0.55
    chunk_size_tokens: int = 400
    chunk_overlap_tokens: int = 60

    # --- Rate limiting ---
    rate_limit_per_minute: int = 30

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance. Import get_settings() wherever config
    is needed instead of instantiating Settings() directly — this
    guarantees the .env file is parsed only once per process.
    """
    return Settings()
