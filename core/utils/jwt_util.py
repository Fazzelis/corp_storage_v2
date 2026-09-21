from datetime import datetime, timezone, timedelta
from core.enums.jwt_type import TokenType
from core.dto.JwtPayload import JwtPayload
from configuration import Config
from core.exceptions.jwt_exceptions import JwtTypeNotFoundException
from uuid import uuid4
import jwt


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
