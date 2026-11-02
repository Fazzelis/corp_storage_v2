from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID
from core.enums.jwt_type import TokenType


@dataclass
class JwtPayload:
    sub: str
    type: TokenType
    exp: Optional[datetime] = None
    iat: Optional[datetime] = None
    jti: Optional[str] = None


@dataclass
class JwtDecodedData:
    sub: UUID
    type: TokenType
    jti: str
    iat: datetime
    exp: datetime
