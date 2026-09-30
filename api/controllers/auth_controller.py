from fastapi import APIRouter, Depends
from core.services.auth_service import AuthService
from core.dependencies import get_auth_service
from api.schemas.auth_schemas import UserRegistrateResponse


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
