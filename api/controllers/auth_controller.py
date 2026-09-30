from fastapi import APIRouter, Depends
from core.services.auth_service import AuthService
from core.dependencies import get_auth_service
from api.schemas.auth_schemas import UserRegistrateResponse, LoginRequest, LoginResponse


router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)


@router.post("/registration", response_model=UserRegistrateResponse)
async def registrate(
        employee_email: str,
        auth_service: AuthService = Depends(get_auth_service)
) -> UserRegistrateResponse:
    created_user = await auth_service.registrate_employee(email=employee_email)
    return UserRegistrateResponse(
        id=created_user.id,
        email=created_user.email
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
