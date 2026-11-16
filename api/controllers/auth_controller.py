from fastapi import APIRouter, Depends, Response
from core.services.auth_service import AuthService
from core.dependencies import get_auth_service
from api.schemas.auth_schemas import (
    RegistrateRequest,
    RegistrateResponse,
    LoginRequest,
    TokenInfoResponse,
    LoginResponse,
)
from configuration import settings

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)


@router.post("/registration", response_model=RegistrateResponse)
async def registrate(
        payload: RegistrateRequest,
        auth_service: AuthService = Depends(get_auth_service)
) -> RegistrateResponse:
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
    )
