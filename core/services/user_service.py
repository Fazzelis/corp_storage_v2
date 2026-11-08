from core.repositories.user_repository import UserRepository
from core.exceptions.user_exceptions import UserNotFound
from core.dto.user_dto import PasswordChangedDto
from core.utils.hasher import hasher
from uuid import UUID

class UserService:
    def __init__(self, user_repo: UserRepository):
        self._user_repository: UserRepository = user_repo

    async def change_password(self, user_id: UUID, new_password: str):
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound
        update_payload = {"password": hasher.hash(new_password), "must_change_password": False}
        await self._user_repository.patch_user(user_id=user.id, payload=update_payload)

        return PasswordChangedDto(message="Пароль успешно изменен")
