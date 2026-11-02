from datetime import datetime, timezone, timedelta
from core.enums.jwt_type import TokenType
from core.dto.JwtDtos import JwtPayload, JwtDecodedData
from configuration import Config
from core.exceptions.jwt_exceptions import JwtTypeNotFoundException, JwtDecodeErrorException
from uuid import uuid4, UUID
import jwt
from jwt import DecodeError


class JwtCodec:
    def __init__(self, settings: Config):
        self._settings = settings

    def encode(self, user_id: UUID, token_type: TokenType) -> str:
        if token_type == TokenType.ACCESS:
            token_ttl = self._settings.access_token_ttl
        elif token_type == TokenType.REFRESH:
            token_ttl = self._settings.refresh_token_ttl
        else:
            raise JwtTypeNotFoundException()

        now = datetime.now(timezone.utc)

        encode = jwt.encode(
            payload={
                "sub": str(user_id),
                "type": token_type.value,
                "jti": str(uuid4()),
                "iat": now,
                "exp": now + timedelta(minutes=token_ttl),
            },
            key=self._settings.private_key,
            algorithm=self._settings.algorithm
        )

        return encode

    def decode(self, token: str):
        try:
            decoded = jwt.decode(
                jwt=token,
                key=self._settings.public_key,
                algorithms=[self._settings.algorithm],
                options={"required": ["sub", "type", "jti", "iat", "exp"]},
            )
            return JwtDecodedData(
                sub=decoded["sub"],
                type=decoded["type"],
                jti=decoded["jti"],
                iat=decoded["iat"],
                exp=decoded["exp"],
            )
        except DecodeError:
            raise JwtDecodeErrorException()
