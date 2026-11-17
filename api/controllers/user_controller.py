from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.security import HTTPAuthorizationCredentials

from api.schemas.user_schemas import (
    ChangeProfileInfoRequest,
    UserInfoResponse
)
from api.schemas.default_schema import DefaultResponse
from configuration import settings
from core.dependencies import get_user_service, get_jwt_codec
from core.enums.jwt_type import TokenType
from core.services.user_service import UserService
from core.utils.jwt_util import JwtCodec

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("/profile")
async def get_profile(
    credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
    user_service: UserService = Depends(get_user_service),
    jwt_codec: JwtCodec = Depends(get_jwt_codec)
):
    access_token = jwt_codec.decode(token=credentials.credentials, expected_type=TokenType.ACCESS)
    user_dto = await user_service.get_user(user_id=access_token.sub)
    return UserInfoResponse.model_validate(user_dto)


@router.patch("/change-profile-info", response_model=UserInfoResponse | DefaultResponse)
async def change_profile_info(
        payload: ChangeProfileInfoRequest,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        user_service: UserService = Depends(get_user_service),
        jwt_codec: JwtCodec = Depends(get_jwt_codec)
) -> UserInfoResponse | DefaultResponse:
    access_token = jwt_codec.decode(token=credentials.credentials, expected_type=TokenType.ACCESS)
    payload_dict = payload.model_dump(exclude_unset=True)
    if len(payload_dict) == 0:
        return DefaultResponse(message="Обновлять нечего")
    result = await user_service.patch_user(user_id=access_token.sub, payload=payload.model_dump(exclude_unset=True))
    return UserInfoResponse.model_validate(result)


@router.post("/change-profile-info/avatar")
async def change_avatar(
        avatar: UploadFile = File(...),
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        user_service: UserService = Depends(get_user_service),
        jwt_codec: JwtCodec = Depends(get_jwt_codec)
):
    decoded_jwt = jwt_codec.decode(token=credentials.credentials, expected_type=TokenType.ACCESS)
    result = await user_service.set_avatar(avatar=avatar, user_id=decoded_jwt.sub)

    return DefaultResponse(message=result.message)
