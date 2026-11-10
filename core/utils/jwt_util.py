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

    def encode(self, user_id: UUID, token_type: TokenType, family_id: UUID | None = None) -> tuple[str, dict]:
        if token_type == TokenType.ACCESS:
            token_ttl = self._settings.access_token_ttl
        elif token_type == TokenType.REFRESH:
            token_ttl = self._settings.refresh_token_ttl
        else:
            raise JwtTypeNotFoundException()

        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "type": token_type.value,
            "jti": str(uuid4()),
            "iat": now,
            "exp": now + timedelta(minutes=token_ttl),
            "role": UserRoleEnum.EMPLOYER.value,
        }
        if token_type == TokenType.REFRESH:
            if family_id is not None:
                payload["family_id"] = str(family_id)
            else:
                payload["family_id"] = str(uuid4())

        encode = jwt.encode(
            payload=payload,
            key=self._settings.private_key,
            algorithm=self._settings.algorithm
        )

        return encode, payload

    def decode(self, token: str, expected_type: TokenType) -> JwtDecodedData:
        try:
            decoded = jwt.decode(
                jwt=token,
                key=self._settings.public_key,
                algorithms=[self._settings.algorithm],
                options={"required": ["sub", "type", "jti", "iat", "exp", "role"]},
            )
            if decoded.get("type") != expected_type.value:
                raise WrongTokenTypeException()
            if expected_type == TokenType.REFRESH and "family_id" not in decoded:
                raise TokenDecodeException()
            return JwtDecodedData(
                sub=decoded["sub"],
                type=decoded["type"],
                jti=decoded["jti"],
                iat=decoded["iat"],
                exp=decoded["exp"],
                role=decoded["role"],
                family_id=decoded.get("family_id")
            )
        except ExpiredSignatureError:
            raise ExpiredTokenException()
        except InvalidTokenError:
            raise TokenDecodeException()
