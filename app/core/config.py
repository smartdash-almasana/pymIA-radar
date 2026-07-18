from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    app_secret: str = "change-me"
    database_url: str = "postgresql+psycopg://inlakech:inlakech@postgres:5432/inlakech"
    openai_api_key: str | None = None
    openai_model: str | None = None
    relaticle_base_url: str = "http://relaticle:8080"
    relaticle_api_token: str | None = None
    last30days_path: str = "/opt/last30days-skill"
    search_interval_minutes: int = 180

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
