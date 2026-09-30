from core.repositories.user_repository import UserRepository
from core.exceptions.auth_exceptions import UserAlreadyRegistered, InvalidLoginOrPassword
from core.utils.password_generator import default_password_generator
from core.dto.auth_dto import SuccessfulUserRegistration, SuccessfulUserLogin
from core.utils.hasher import hasher


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self._user_repository: UserRepository = user_repo

    async def registrate_employee(self, email: str) -> SuccessfulUserRegistration:
        user = await self._user_repository.get_by_email(email)
        if user:
            raise UserAlreadyRegistered()

        created_user = await self._user_repository.post(
            email=email,
            password=hasher.hash(default_password_generator.generate_password())
        )
        return SuccessfulUserRegistration(
            id=created_user.id,
            email=created_user.email
        )

    async def login(self, email: str, password: str) -> SuccessfulUserLogin:
        user = await self._user_repository.get_by_email(email)
        if not user or not hasher.verify(password, user.password):
            raise InvalidLoginOrPassword()

        return SuccessfulUserLogin(
            id=user.id,
            email=user.email,
            name=user.name,
            surname=user.surname,
            patronymic=user.patronymic,
            avatar_path=user.avatar_path
        )
