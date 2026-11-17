from fastapi import APIRouter, Depends, Response, HTTPException, status, Cookie
from fastapi.security import HTTPAuthorizationCredentials

from core.dto.auth_dto import RecoveryTicketDto
from core.services.auth_service import AuthService
from core.dependencies import get_auth_service, get_jwt_codec
from api.schemas.auth_schemas import (
    RegistrateRequest,
    LoginRequest,
    TokenInfoResponse,
    LoginResponse,
    SendRecoveryCodeRequest,
    SendRecoveryCodeResponse,
    VerifyRecoveryCodeRequest,
    VerifyRecoveryCodeResponse,
    ChangePasswordRequest,
    ChangePasswordResponse
)
from api.schemas.default_schema import DefaultSchema
from configuration import settings
from core.utils.jwt_util import JwtCodec
from core.enums.jwt_type import TokenType
from core.enums.user_role_enum import UserRoleEnum

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)


@router.post("/registration", response_model=DefaultSchema)
async def registrate(
        payload: RegistrateRequest,
        jwt_codec: JwtCodec = Depends(get_jwt_codec),
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        auth_service: AuthService = Depends(get_auth_service)
) -> DefaultSchema:
    access_token = jwt_codec.decode(credentials.credentials, TokenType.ACCESS)
    if access_token.role != UserRoleEnum.DIRECTOR.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет прав"
        )
    await auth_service.registrate_employee(
        email=payload.email,
        name=payload.name,
        surname=payload.surname,
        patronymic=payload.patronymic
    )
    return DefaultSchema(
        message="Пользователь успешно зарегистрирован!"
    )


@router.post("/login")
async def login(
        payload: LoginRequest,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service)
) -> LoginResponse | VerifyRecoveryCodeResponse:
    result = await auth_service.login(payload.email, payload.password)

    if isinstance(result, RecoveryTicketDto):
        return VerifyRecoveryCodeResponse(
            recovery_ticket=result.recovery_ticket
        )

    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=settings.refresh_token_ttl_for_browser
    )

    return LoginResponse(
        token=TokenInfoResponse(
            token=result.access_token,
            type="Bearer"
        ),
        must_change_password=result.must_change_password
    )


@router.get("/refresh", response_model=TokenInfoResponse)
async def refresh(
        response: Response,
        refresh_token: str | None = Cookie(default=None),
        auth_service: AuthService = Depends(get_auth_service),
        jwt_codec: JwtCodec = Depends(get_jwt_codec),
) -> TokenInfoResponse:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh токен не найден"
        )
    decoded_refresh_token = jwt_codec.decode(refresh_token, expected_type=TokenType.REFRESH)
    result = await auth_service.refresh(old_refresh_token=decoded_refresh_token)

    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=settings.refresh_token_ttl_for_browser
    )

    return TokenInfoResponse(
        token=result.access_token,
        type="Bearer"
    )


@router.post("/logout", response_model=DefaultSchema)
async def logout(
        response: Response,
        refresh_token: str | None = Cookie(default=None),
        auth_service: AuthService = Depends(get_auth_service),
        jwt_codec: JwtCodec = Depends(get_jwt_codec),
) -> DefaultSchema:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh токен не найден"
        )
    decoded_refresh_token = jwt_codec.decode(refresh_token, expected_type=TokenType.REFRESH)
    result = await auth_service.logout(refresh_token=decoded_refresh_token)

    response.delete_cookie(key="refresh_token", secure=True, samesite='none', httponly=True)

    return DefaultSchema(message=result.message)


@router.post("/password-recovery/send-code", response_model=SendRecoveryCodeResponse)
async def send_recovery_password(
        payload: SendRecoveryCodeRequest,
        auth_service: AuthService = Depends(get_auth_service)
) -> SendRecoveryCodeResponse:
    result = await auth_service.send_recovery_code(email=payload.email)
    return SendRecoveryCodeResponse(
        message=result.message
    )


@router.post("/password-recovery/verify-code", response_model=VerifyRecoveryCodeResponse)
async def verify_recovery_code(
        payload: VerifyRecoveryCodeRequest,
        auth_service: AuthService = Depends(get_auth_service)
) -> VerifyRecoveryCodeResponse:
    result = await auth_service.verify_recovery_code(email=payload.email, recovery_code=payload.recovery_code)
    return VerifyRecoveryCodeResponse(
        recovery_ticket=result.recovery_ticket
    )

@router.post("/password-recovery/change-password", response_model=ChangePasswordResponse)
async def change_password(
        payload: ChangePasswordRequest,
        auth_service: AuthService = Depends(get_auth_service)
) -> ChangePasswordResponse:
    result = await auth_service.change_password(
        recovery_ticket=payload.recovery_ticket,
        new_password=payload.new_password
    )
    return ChangePasswordResponse(
        message=result.message
    )
