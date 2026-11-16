from configuration import settings, Config
from core.services.user_service import UserService
from core.utils.jwt_util import JwtCodec
from core.services.auth_service import AuthService
from core.repositories.user_repository import UserRepository
from database.database import get_db
from fastapi import Depends


def get_settings() -> Config:
    return settings

def get_jwt_codec(settings=Depends(get_settings)) -> JwtCodec:
    return JwtCodec(settings)


def get_auth_service(db_session=Depends(get_db)):
    return AuthService(user_repo=UserRepository(db_session=db_session))


def get_user_service(db_session=Depends(get_db)):
    return UserService(user_repo=UserRepository(db_session=db_session))
