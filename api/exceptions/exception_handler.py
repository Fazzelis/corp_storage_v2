from core.exceptions.auth_exceptions import (
    UserAlreadyRegistered,
    InvalidLoginOrPassword
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
