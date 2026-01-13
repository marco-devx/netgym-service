from functools import lru_cache

from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(".env", override=True)


class Settings(BaseSettings):
    app_env: str
    python_path: str
    allowed_origins: list[str] = []

    db_user: str
    db_pass: str
    db_host: str
    db_port: int
    db_name: str

    baseball_data_url: str = "https://resource-hub-production.s3.us-west-2.amazonaws.com/uploads/62/baseball_data.json"
    openai_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def split_origins(cls, value):
        if isinstance(value, str):
            return [x.strip() for x in value.split(",")]
        return value


@lru_cache()
def get_settings() -> Settings:
    return Settings()
