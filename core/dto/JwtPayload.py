from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from core.enums.jwt_type import TokenType


@dataclass
class JwtPayload:
    sub: str
    type: TokenType
    exp: Optional[datetime] = None
    iat: Optional[datetime] = None
    jti: Optional[str] = None
