from configuration import settings, Config
from core.utils.jwt_util import JwtCodec


def get_settings() -> Config:
    return settings


def get_jwt_codec(settings: Config) -> JwtCodec:
    return JwtCodec(settings)
