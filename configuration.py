from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar
from fastapi.security import HTTPBearer


class Config(BaseSettings):
    access_token_ttl: int = 30
    refresh_token_ttl: int = 20160
    access_token_ttl_for_browser: int = access_token_ttl*60
    refresh_token_ttl_for_browser: int = refresh_token_ttl*60
    http_bearer: ClassVar = HTTPBearer()
    database_url: str
    algorithm: str
    private_key: str
    public_key: str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Config()
