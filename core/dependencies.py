from configuration import settings, Config
from core.utils.jwt_util import JwtCodec
from core.services.auth_service import AuthService
from core.repositories.user_repository import UserRepository
from database.database import get_db
from fastapi import Depends


def get_settings() -> Config:
    return settings


def get_jwt_codec(settings: Config) -> JwtCodec:
    return JwtCodec(settings)


def get_auth_service(db_session=Depends(get_db)):
    return AuthService(user_repo=UserRepository(db_session=db_session))
