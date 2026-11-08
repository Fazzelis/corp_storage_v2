from fastapi import FastAPI
from core.exceptions.auth_exceptions import UserAlreadyRegistered, InvalidLoginOrPassword
from core.exceptions.jwt_exceptions import (
    JwtTypeNotFoundException,
    ExpiredTokenException,
    WrongTokenTypeException,
    TokenDecodeException
)
from api.exceptions.exception_handler import ExceptionHandler


def registrate_all_exceptions(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyRegistered,
        ExceptionHandler.user_already_exist_handler
    )
    app.add_exception_handler(
        InvalidLoginOrPassword,
        ExceptionHandler.invalid_login_or_password_handler
    )
    app.add_exception_handler(
        JwtTypeNotFoundException,
        ExceptionHandler.jwt_type_not_found_handler
    )
    app.add_exception_handler(
        ExpiredTokenException,
        ExceptionHandler.expired_token_handler
    )
    app.add_exception_handler(
        WrongTokenTypeException,
        ExceptionHandler.wrong_token_type_handler
    )
    app.add_exception_handler(
        TokenDecodeException,
        ExceptionHandler.token_decode_exception_handler
    )
