from configuration import settings
from core.models import User
from core.repositories.user_repository import UserRepository
from core.exceptions.user_exceptions import UserNotFound, UserMustChangePassword
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
from core.dto.user_dto import UserDto, UserShortDto

import magic
from uuid import UUID, uuid4
from typing import cast
from fastapi import UploadFile
from PIL import Image, UnidentifiedImageError
from pathlib import Path

from core.dto.default_dto import DefaultDto


class UserService:
    def __init__(self, user_repo: UserRepository):
        self._user_repository: UserRepository = user_repo

    async def get_user(self, user_id: UUID) -> UserDto:
        user = await self._user_repository.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFound()
        if user.must_change_password:
            raise UserMustChangePassword()
        return UserDto(
            email=user.email,
            name=user.name,
            surname=user.surname,
            patronymic=user.patronymic,
            avatar_path=user.avatar_path,
            must_change_password=user.must_change_password
        )

    async def get_short_profile_info(self, user_id: UUID):
        user = await self._user_repository.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFound()
        if user.must_change_password:
            raise UserMustChangePassword()
        return UserShortDto(
            name=user.name,
            surname=user.surname,
            role=user.role.value
        )

    async def patch_user(self, user_id: UUID, payload: dict) -> UserDto:
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound
        if user.must_change_password:
            raise UserMustChangePassword()
        await self._user_repository.patch_user(user_id=user.id, payload=payload)
        updated_user = cast(User, await self._user_repository.get_by_id(user.id))

        return UserDto(
            email=updated_user.email,
            name=updated_user.name,
            surname=updated_user.surname,
            patronymic=updated_user.patronymic,
            avatar_path=updated_user.avatar_path,
            must_change_password=updated_user.must_change_password
        )

    async def set_avatar(self, avatar: UploadFile, user_id: UUID) -> DefaultDto:
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        head = avatar.file.read(1)
        if not head:
            raise EmptyAvatarException()
        avatar.file.seek(0)

        head = avatar.file.read(2048)
        detected_mime = magic.from_buffer(head, mime=True)
        avatar.file.seek(0)
        if detected_mime not in settings.avatar_mimes:
            raise UnsupportedAvatarTypeException()

        try:
            with Image.open(avatar.file, formats=["JPEG", "PNG"]) as img:
                if img.format not in settings.avatar_fil_formats:
                    raise UnsupportedAvatarTypeException()
                if img.width > settings.avatar_max_resolution or img.height > settings.avatar_max_resolution:
                    raise TooBigResolutionAvatarException(max_resolution=settings.avatar_max_resolution)
                if img.width == 0 or img.height == 0:
                    raise TooSmallResolutionAvatarException()
                img.verify()
        except UnidentifiedImageError:
            raise NotImageAvatarException()
        finally:
            avatar.file.seek(0)

        ext = settings.avatar_mimes[detected_mime]
        file_name = f"{uuid4().hex}{ext}"
        file_path = Path(settings.avatars_dir) / file_name

        total_size = 0
        try:
            with file_path.open("xb") as output:
                chunk = avatar.file.read(1024*1024)
                while chunk:
                    total_size += len(chunk)
                    if total_size > settings.avatar_file_max_size*1024*1024:
                        raise TooBigFileSizeAvatarException()
                    output.write(chunk)
                    chunk = avatar.file.read(1024 * 1024)
            await self._user_repository.patch_user(
                user_id=user.id,
                payload={
                    "avatar_path": str(file_path)
                }
            )
            return DefaultDto(message="Аватарка успешно сохранена!")
        except TooBigFileSizeAvatarException as e:
            if file_path.exists():
                file_path.unlink()
            raise e
        except Exception:
            import traceback
            traceback.print_exc()
            raise FailToWriteAvatarException()

    async def get_avatar_path(self, user_id: UUID) -> Path | None:
        user = await self._user_repository.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFound()

        if not user.avatar_path:
            return None

        file_path = Path(user.avatar_path)
        if not file_path.is_file():
            raise ImageNotFoundAvatarException()

        return file_path
