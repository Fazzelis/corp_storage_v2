from core.exceptions.auth_exceptions import (
    UserAlreadyRegistered,
    InvalidLoginOrPassword
)
from core.exceptions.jwt_exceptions import (
    JwtTypeNotFoundException,
    ExpiredTokenException,
    WrongTokenTypeException,
    TokenDecodeException
)
from fastapi import HTTPException, status


class ExceptionHandler:
    def __init__(self):
        pass

    async def user_already_exist_handler(self, exc: UserAlreadyRegistered):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        )

    async def invalid_login_or_password_handler(self, exc: InvalidLoginOrPassword):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        )

    async def jwt_type_not_found_handler(self, exc: JwtTypeNotFoundException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc)
        )

    async def expired_token_handler(self, exc: ExpiredTokenException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc)
        )

    async def wrong_token_type_handler(self, exc: WrongTokenTypeException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc)
        )

    async def token_decode_exception_handler(self, exc: TokenDecodeException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc)
        )
