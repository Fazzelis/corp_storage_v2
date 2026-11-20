from core.exceptions.auth_exceptions import (
    UserAlreadyRegistered,
    InvalidLoginOrPassword,
    RefreshTokenNotFound,
    InvalidRecoveryCode,
    InvalidTicket
)
from core.exceptions.avatar_exceptions import (
    EmptyAvatarException,
    UnsupportedAvatarTypeException,
    TooBigResolutionAvatarException,
    TooSmallResolutionAvatarException,
    NotImageAvatarException,
    TooBigFileSizeAvatarException,
    FailToWriteAvatarException,
    ImageNotFoundAvatarException
)
from core.exceptions.jwt_exceptions import (
    JwtTypeNotFoundException,
    ExpiredTokenException,
    WrongTokenTypeException,
    TokenDecodeException
)
from core.exceptions.user_exceptions import (
    UserNotFound,
    UserMustChangePassword
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

    async def refresh_token_not_found_handler(self, exc: RefreshTokenNotFound):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc)
        )

    async def invalid_recover_code_handler(self, exc: InvalidRecoveryCode):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )

    async def invalid_ticket_handler(self, exc: InvalidTicket):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
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

    async def user_not_found_exception_handler(self, exc: UserNotFound):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )

    async def user_must_change_password_exception_handler(self, exc: UserMustChangePassword):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc)
        )

    async def empty_avatar_exception_handler(self, exc: EmptyAvatarException):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )

    async def unsupported_avatar_type_exception_handler(self, exc: UnsupportedAvatarTypeException):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )

    async def too_big_resolution_avatar_exception_handler(self, exc: TooBigResolutionAvatarException):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )

    async def too_small_resolution_avatar_exception_handler(self, exc: TooSmallResolutionAvatarException):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )

    async def not_a_image_avatar_exception_handler(self, exc: NotImageAvatarException):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )

    async def too_big_file_size_avatar_exception_handler(self, exc: TooBigFileSizeAvatarException):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )

    async def fail_to_write_avatar_exception_handler(self, exc: FailToWriteAvatarException):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )

    async def image_not_found_avatar_exception_handler(self, exc: ImageNotFoundAvatarException):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )
