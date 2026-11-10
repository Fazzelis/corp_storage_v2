from core.dto.JwtDtos import JwtDecodedData
from core.enums.jwt_type import TokenType
from core.repositories.user_repository import UserRepository
from core.exceptions.auth_exceptions import (
    UserAlreadyRegistered,
    InvalidLoginOrPassword,
    RefreshTokenNotFound
)
from core.utils.jwt_util import JwtCodec
from core.utils.password_generator import default_password_generator
from core.dto.auth_dto import (
    SuccessfulUserRegistration,
    SuccessfulUserLogin,
    SuccessfulRefresh
)
from core.utils.hasher import hasher
from configuration import settings
from core.utils.mail_sender import MailSender
from core.repositories.refresh_token_repository import RefreshTokenRepository
from core.enums.refresh_token_status_enum import RefreshTokenStatusEnum

from logging import getLogger
from uuid import UUID


class AuthService:
    def __init__(self, user_repo: UserRepository, refresh_token_repo: RefreshTokenRepository):
        self._user_repository: UserRepository = user_repo
        self._refresh_token_repository: RefreshTokenRepository = refresh_token_repo
        self._jwtCodec: JwtCodec = JwtCodec(settings)
        self.logger = getLogger()
        self._mail_sender: MailSender = MailSender()

    async def registrate_employee(
            self,
            email: str,
            name: str,
            surname: str,
            patronymic: str | None
    ) -> SuccessfulUserRegistration:
        user = await self._user_repository.get_by_email(email)
        if user:
            raise UserAlreadyRegistered()

        password = default_password_generator.generate_password()
        self.logger.info(f"Пароль от {email}: {password}")

        await self._mail_sender.send_verify_code(to_email=email, code=password)

        created_user = await self._user_repository.post(
            email=email,
            password=hasher.hash(password),
            name=name,
            surname=surname,
            patronymic=patronymic
        )
        return SuccessfulUserRegistration(
            id=created_user.id,
            email=created_user.email,
            name=created_user.name,
            surname=created_user.surname,
            patronymic=created_user.patronymic,
            avatar_path=created_user.avatar_path
        )

    async def login(self, email: str, password: str) -> SuccessfulUserLogin:
        user = await self._user_repository.get_by_email(email)
        if not user or not hasher.verify(password, user.password):
            raise InvalidLoginOrPassword()

        access_token, _ = self._jwtCodec.encode(user_id=user.id, token_type=TokenType.ACCESS)
        refresh_token, refresh_info = self._jwtCodec.encode(user_id=user.id, token_type=TokenType.REFRESH)

        await self._refresh_token_repository.post(
            jti=refresh_info["jti"],
            family_id=refresh_info["family_id"],
            status=RefreshTokenStatusEnum.ACTIVE,
            expires_at=refresh_info["exp"],
            created_at=refresh_info["iat"],
            user_id=user.id
        )

        return SuccessfulUserLogin(
            id=user.id,
            email=user.email,
            name=user.name,
            surname=user.surname,
            access_token=access_token,
            refresh_token=refresh_token,
            patronymic=user.patronymic,
            avatar_path=user.avatar_path
        )

    async def refresh(self, old_refresh_token: JwtDecodedData) -> SuccessfulRefresh:
        old_refresh_token_db = await self._refresh_token_repository.get_by_jti(jti=UUID(old_refresh_token.jti))
        if not old_refresh_token_db:
            raise RefreshTokenNotFound()
        await self._refresh_token_repository.set_rotated(jti=old_refresh_token_db.jti)

        access_token, _ = self._jwtCodec.encode(
            user_id=old_refresh_token_db.user_id,
            token_type=TokenType.ACCESS
        )
        refresh_token, refresh_info = self._jwtCodec.encode(
            user_id=old_refresh_token_db.user_id,
            token_type=TokenType.REFRESH,
            family_id=old_refresh_token_db.family_id
        )

        await self._refresh_token_repository.post(
            jti=refresh_info["jti"],
            family_id=refresh_info["family_id"],
            status=RefreshTokenStatusEnum.ACTIVE,
            expires_at=refresh_info["exp"],
            created_at=refresh_info["iat"],
            user_id=old_refresh_token_db.user_id
        )

        return SuccessfulRefresh(
            access_token=access_token,
            refresh_token=refresh_token,
        )
