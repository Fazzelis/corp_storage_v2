from core.enums.jwt_type import TokenType
from core.dto.JwtDtos import JwtPayload, JwtDecodedData
from configuration import Config
from core.exceptions.jwt_exceptions import (
    JwtTypeNotFoundException,
    ExpiredTokenException,
    WrongTokenTypeException,
    TokenDecodeException
)
from core.enums.user_role_enum import UserRoleEnum

from datetime import datetime, timezone, timedelta
from uuid import uuid4, UUID
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError


class JwtCodec:
    def __init__(self, settings: Config):
        self._settings = settings

    def encode(self, user_id: UUID, token_type: TokenType) -> tuple[str, JwtPayload]:
        if token_type == TokenType.ACCESS:
            token_ttl = self._settings.access_token_ttl
        elif token_type == TokenType.REFRESH:
            token_ttl = self._settings.refresh_token_ttl
        else:
            raise JwtTypeNotFoundException()

        now = datetime.now(timezone.utc)
        payload = JwtPayload(
            sub=user_id,
            type=token_type,
            jti=uuid4(),
            iat=now,
            exp=now + timedelta(minutes=token_ttl),
            role=UserRoleEnum.EMPLOYER,
            family_id=uuid4(),
        )

        encode = jwt.encode(
            payload={
                "sub": str(payload.sub),
                "type": payload.type.value,
                "jti": str(payload.jti),
                "iat": payload.iat,
                "exp": payload.exp,
                "role": payload.role.value,
                "family_id": str(payload.family_id),
            },
            key=self._settings.private_key,
            algorithm=self._settings.algorithm
        )

        return encode, payload

    def decode(self, token: str, expected_type: TokenType):
        try:
            decoded = jwt.decode(
                jwt=token,
                key=self._settings.public_key,
                algorithms=[self._settings.algorithm],
                options={"required": ["sub", "type", "jti", "iat", "exp", "role", "family_id"]},
            )
            if decoded.get("type") != expected_type.value:
                raise WrongTokenTypeException()
            return JwtDecodedData(
                sub=decoded["sub"],
                type=decoded["type"],
                jti=decoded["jti"],
                iat=decoded["iat"],
                exp=decoded["exp"],
                role=decoded["role"],
                family_id=decoded["family_id"]
            )
        except ExpiredSignatureError:
            raise ExpiredTokenException()
        except InvalidTokenError:
            raise TokenDecodeException()
