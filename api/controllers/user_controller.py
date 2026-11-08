from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials

from api.schemas.user_schemas import ChangePasswordRequest, ChangePasswordResponse
from configuration import settings
from core.dependencies import get_user_service, get_jwt_codec
from core.enums.jwt_type import TokenType
from core.services.user_service import UserService
from core.utils.jwt_util import JwtCodec

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/change-password")
async def change_password(
        payload: ChangePasswordRequest,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        user_service: UserService = Depends(get_user_service),
        jwt_codec: JwtCodec = Depends(get_jwt_codec)
):
    access_token = jwt_codec.decode(token=credentials.credentials, expected_type=TokenType.ACCESS)
    result = await user_service.change_password(user_id=UUID(access_token.sub), new_password=payload.new_password)
    return ChangePasswordResponse(
        message=result.message
    )
