from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="huggingface-chatbot", validation_alias="APP_NAME")
    app_env: Literal["local", "dev", "test", "staging", "prod"] = Field(
        default="local", validation_alias="APP_ENV"
    )
    debug: bool = Field(default=False, validation_alias="APP_DEBUG")
    api_v1_prefix: str = Field(default="/api/v1", validation_alias="API_V1_PREFIX")
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/huggingface_chatbot",
        validation_alias="DATABASE_URL",
    )
    model_name: str = "Qwen/Qwen2.5-0.5B-Instruct"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
