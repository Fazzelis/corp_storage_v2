from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, timezone

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

    async def get_by_jti(self, jti: UUID) -> RefreshToken | None:
        result = await self._db.execute(select(RefreshToken).where(RefreshToken.jti == jti))
        return result.scalar_one_or_none()

    async def set_rotated(self, jti: UUID):
        await self._db.execute(
            update(RefreshToken)
            .where(
                RefreshToken.jti == jti,
                RefreshToken.status == RefreshTokenStatusEnum.ACTIVE
            )
            .values(
                rotated_at=datetime.now(timezone.utc),
                status=RefreshTokenStatusEnum.ROTATED
            )
        )
        await self._db.commit()
