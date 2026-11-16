from fastapi import APIRouter, Depends, Response, HTTPException, status, Cookie
from fastapi.security import HTTPAuthorizationCredentials

from core.services.auth_service import AuthService
from core.dependencies import get_auth_service, get_jwt_codec
from api.schemas.auth_schemas import (
    RegistrateRequest,
    RegistrateResponse,
    LoginRequest,
    TokenInfoResponse,
    LoginResponse,
    SendRecoveryCodeRequest,
    SendRecoveryCodeResponse,
    VerifyRecoveryCodeRequest,
    VerifyRecoveryCodeResponse
)
from configuration import settings
from core.utils.jwt_util import JwtCodec
from core.enums.jwt_type import TokenType
from core.enums.user_role_enum import UserRoleEnum

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)


@router.post("/registration", response_model=RegistrateResponse)
async def registrate(
        payload: RegistrateRequest,
        jwt_codec: JwtCodec = Depends(get_jwt_codec),
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        auth_service: AuthService = Depends(get_auth_service)
) -> RegistrateResponse:
    access_token = jwt_codec.decode(credentials.credentials, TokenType.ACCESS)
    if access_token.role != UserRoleEnum.DIRECTOR.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет прав"
        )
    created_user = await auth_service.registrate_employee(
        email=payload.email,
        name=payload.name,
        surname=payload.surname,
        patronymic=payload.patronymic
    )
    return RegistrateResponse(
        id=str(created_user.id),
        email=created_user.email,
        name=created_user.name,
        surname=created_user.surname,
        patronymic=created_user.patronymic,
        avatar_path=created_user.avatar_path
    )


@router.post("/login", response_model=LoginResponse)
async def login(
        payload: LoginRequest,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service)
) -> LoginResponse:
    user_info = await auth_service.login(payload.email, payload.password)

    response.set_cookie(
        key="refresh_token",
        value=user_info.refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=settings.refresh_token_ttl_for_browser
    )

    return LoginResponse(
        id=str(user_info.id),
        email=user_info.email,
        name=user_info.name,
        surname=user_info.surname,
        token=TokenInfoResponse(
            token=user_info.access_token,
            type="Bearer"
        ),
        patronymic=user_info.patronymic,
        avatar_path=user_info.avatar_path,
        must_change_password=user_info.must_change_password
    )


@router.get("/refresh", response_model=TokenInfoResponse)
async def refresh(
        response: Response,
        refresh_token: str | None = Cookie(default=None),
        auth_service: AuthService = Depends(get_auth_service),
        jwt_codec: JwtCodec = Depends(get_jwt_codec),
):
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


@router.post("/password-recovery/send-code", response_model=SendRecoveryCodeResponse)
async def send_recover_password(
        payload: SendRecoveryCodeRequest,
        auth_service: AuthService = Depends(get_auth_service)
):
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
        recovery_ticket=result.recovery_ticket,
        expires_at=result.expires_at
    )
