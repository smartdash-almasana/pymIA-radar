from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    app_secret: str = "change-me"
    database_url: str = "postgresql+psycopg://inlakech:inlakech@postgres:5432/inlakech"
    openai_api_key: str | None = None
    openai_model: str | None = None
    semantic_llm_enabled: bool = True
    semantic_llm_provider: str = "agnes"
    semantic_llm_base_url: str | None = "https://apihub.agnes-ai.com/v1"
    semantic_llm_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SEMANTIC_LLM_API_KEY", "AGNES_API_KEY"),
    )
    semantic_llm_model: str | None = "agnes-2.0-flash"
    gemini_api_key: str | None = None
    gemini_model: str = "gemma-4-26b-a4b-it"
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"
    relaticle_base_url: str = "http://relaticle:8080"
    relaticle_api_token: str | None = None
    last30days_path: str = "/opt/last30days-skill"
    search_interval_minutes: int = 180

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
