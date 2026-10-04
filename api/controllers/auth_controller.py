from fastapi import APIRouter, Depends
from core.services.auth_service import AuthService
from core.dependencies import get_auth_service
from api.schemas.auth_schemas import (
    RegistrateRequest,
    RegistrateResponse,
    LoginRequest,
    LoginResponse
)


router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)


@router.post("/registration", response_model=RegistrateResponse)
async def registrate(
        payload: RegistrateRequest,
        auth_service: AuthService = Depends(get_auth_service)
) -> RegistrateResponse:
    created_user = await auth_service.registrate_employee(payload)
    return RegistrateResponse(
        id=created_user.id,
        email=created_user.email,
        name=created_user.name,
        surname=created_user.surname,
        patronymic=created_user.patronymic,
        avatar_path=created_user.avatar_path
    )


@router.post("/login", response_model=LoginResponse)
async def login(
        payload: LoginRequest,
        auth_service: AuthService = Depends(get_auth_service)
) -> LoginResponse:
    user_info = await auth_service.login(payload.email, payload.password)
    return LoginResponse(
        id=user_info.id,
        email=user_info.email,
        name=user_info.name,
        surname=user_info.surname,
        patronymic=user_info.patronymic,
        avatar_path=user_info.avatar_path
    )
