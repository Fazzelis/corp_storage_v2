from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar
from fastapi.security import HTTPBearer


class Config(BaseSettings):
    # JWT
    access_token_ttl: int = 30
    refresh_token_ttl: int = 20160
    access_token_ttl_for_browser: int = access_token_ttl*60
    refresh_token_ttl_for_browser: int = refresh_token_ttl*60
    http_bearer: ClassVar = HTTPBearer()
    algorithm: str
    # Код и тикет восстановления пароля
    recovery_code_ttl: int = 10 # минуты
    recovery_ticket_ttl: int = 2 # минуты
    # База данных
    database_url: str
    # Ключи для JWT
    private_key: str
    public_key: str
    # Настройки генератора пароля/кода
    generated_password_alphabet: str
    generated_password_len: int
    # Настройки для отправки email сообщений
    smtp_server: str
    smtp_port: int
    email_login: str
    email_password: str
    # Настройки для ssl сертификата
    ssl_certfile: str
    ssl_keyfile: str
    ssl_keyfile_password: str
    # Настройки аватарки
    avatar_file_max_size: int = 2 # МБ
    avatar_max_resolution: int = 4000 # пиксели
    avatar_mimes : dict = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
    }
    avatar_fil_formats: set = {"JPEG", "PNG"}
    avatars_dir: str = "attachments/employer-avatars"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Config()
