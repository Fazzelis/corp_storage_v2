from datetime import datetime, timezone, timedelta
from core.enums.jwt_type import TokenType
from core.dto.JwtDtos import JwtPayload, JwtDecodedData
from configuration import Config
from core.exceptions.jwt_exceptions import JwtTypeNotFoundException, JwtDecodeErrorException
from uuid import uuid4
import jwt
from jwt import DecodeError


class JwtCodec:
    def __init__(self, settings: Config):
        self._settings = settings

    async def encode(self, payload: JwtPayload) -> tuple[str, JwtPayload]:
        if payload.type == TokenType.ACCESS:
            token_ttl = self._settings.access_token_ttl
        elif payload.type == TokenType.REFRESH:
            token_ttl = self._settings.refresh_token_ttl
        else:
            raise JwtTypeNotFoundException()
        now = datetime.now(timezone.utc)

        expiration_time = now + timedelta(minutes=token_ttl)
        jti = uuid4()
        payload.exp = expiration_time
        payload.iat = datetime.now()
        payload.jti = str(jti)

        encode = jwt.encode(
            payload={
                "sub": payload.sub,
                "exp": payload.exp,
                "iat": payload.iat,
                "jti": payload.jti
            },
            key=self._settings.private_key,
            algorithm=self._settings.algorithm
        )

        return encode, payload

    async def decode(self, token: str):
        try:
            decoded = jwt.decode(
                jwt=token,
                key=self._settings.public_key,
                algorithms=[self._settings.algorithm]
            )
            return JwtDecodedData(
                sub=decoded["sub"],
                exp=decoded["exp"],
                iat=decoded["iat"],
                jti=decoded["jti"]
            )
        except DecodeError:
            raise JwtDecodeErrorException()
