from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from core.enums.jwt_type import TokenType
from core.enums.user_role_enum import UserRoleEnum


@dataclass
class JwtPayload:
    sub: UUID
    type: TokenType
    jti: UUID
    iat: datetime
    exp: datetime
    role: UserRoleEnum
    family_id: UUID | None = None


@dataclass
class JwtDecodedData:
    sub: UUID
    type: TokenType
    jti: str
    iat: datetime
    exp: datetime
    role: UserRoleEnum
    family_id: UUID | None = None
