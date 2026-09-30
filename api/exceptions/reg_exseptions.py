from fastapi import FastAPI
from core.exceptions.auth_exceptions import UserAlreadyRegistered, InvalidLoginOrPassword
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
