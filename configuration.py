from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar
from fastapi.security import HTTPBearer


class Config(BaseSettings):
    access_token_ttl: int = 30
    refresh_token_ttl: int = 20160
    access_token_ttl_for_browser: int = access_token_ttl*60
    refresh_token_ttl_for_browser: int = refresh_token_ttl*60
    recovery_code_ttl: int = 10 # minutes
    recovery_ticket_ttl: int = 2 # minutes
    http_bearer: ClassVar = HTTPBearer()
    database_url: str
    algorithm: str
    private_key: str
    public_key: str
    generated_password_alphabet: str
    generated_password_len: int
    smtp_server: str
    smtp_port: int
    email_login: str
    email_password: str
    ssl_certfile: str
    ssl_keyfile: str
    ssl_keyfile_password: str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Config()
