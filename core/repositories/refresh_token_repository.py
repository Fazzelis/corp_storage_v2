from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from core.enums.refresh_token_status_enum import RefreshTokenStatusEnum
from core.models.refresh_token import RefreshToken

class RefreshTokenRepository:
    def __init__(self, db: AsyncSession):
        self._db: AsyncSession = db

    async def post(
            self,
            jti: UUID,
            family_id: UUID,
            status: RefreshTokenStatusEnum,
            expires_at: datetime,
            created_at: datetime,
            user_id: UUID,
            rotated_at: datetime | None = None,
            revoked_at: datetime | None = None
    ) -> RefreshToken:
        token = RefreshToken(
            jti=jti,
            family_id=family_id,
            status=status,
            expires_at=expires_at,
            created_at=created_at,
            user_id=user_id,
            rotated_at=rotated_at,
            revoked_at=revoked_at
        )
        self._db.add(token)
        await self._db.commit()
        await self._db.refresh(token)
        return token
