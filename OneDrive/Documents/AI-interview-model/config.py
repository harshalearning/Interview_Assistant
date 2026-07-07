from pydantic import Field

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:  # pragma: no cover - fallback for older environments
    from pydantic import BaseSettings

    SettingsConfigDict = None


class Settings(BaseSettings):
    """Application settings loaded from environment or .env file."""

    ollama_base_url: str = Field(default="http://127.0.0.1:11434")
    ollama_default_model: str = Field(default="qwen2.5:latest")
    ollama_timeout_seconds: int = Field(default=60)
    ollama_max_tokens: int = Field(default=256)
    ollama_default_temperature: float = Field(default=0.7)

    if SettingsConfigDict is not None:
        model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    else:  # pragma: no cover - legacy pydantic fallback
        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"


settings = Settings()
