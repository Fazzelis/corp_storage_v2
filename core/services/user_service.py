from core.models import User
from core.repositories.user_repository import UserRepository
from core.exceptions.user_exceptions import UserNotFound, UserMustChangePassword
from core.dto.user_dto import PasswordChangedDto, UserDto
from core.utils.hasher import hasher
from uuid import UUID
from typing import cast

class UserService:
    def __init__(self, user_repo: UserRepository):
        self._user_repository: UserRepository = user_repo

    async def get_user(self, user_id: UUID) -> UserDto:
        user = await self._user_repository.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFound
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

    async def change_password(self, user_id: UUID, new_password: str):
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound
        update_payload = {"password": hasher.hash(new_password), "must_change_password": False}
        await self._user_repository.patch_user(user_id=user.id, payload=update_payload)

        return PasswordChangedDto(message="Пароль успешно изменен")

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
