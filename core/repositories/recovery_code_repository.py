from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from core.models.recovery_code import RecoveryCode
from datetime import datetime, timezone, timedelta

from configuration import settings

class RecoveryCodeRepository:
    def __init__(self, db: AsyncSession):
        self._db: AsyncSession = db

    async def post(self, user_id: UUID, code_hash: str) -> RecoveryCode:
        created_at = datetime.now(timezone.utc)
        expires_at = created_at + timedelta(minutes=settings.recovery_code_ttl)
        code_db = RecoveryCode(
            code=code_hash,
            created_at=created_at,
            expires_at=expires_at,
            user_id=user_id
        )
        self._db.add(code_db)
        await self._db.commit()
        await self._db.refresh(code_db)
        return code_db

    async def invalidate(self, recovery_code_id: UUID) -> None:
        await self._db.execute(
            update(RecoveryCode)
            .where(
                RecoveryCode.id == recovery_code_id,
                RecoveryCode.expires_at > datetime.now(timezone.utc)
            )
            .values(used_at=datetime.now(timezone.utc))
        )
        await self._db.commit()

    async def add_attempt(self, recovery_code_id: UUID) -> None:
        await self._db.execute(
            update(RecoveryCode)
            .where(RecoveryCode.id == recovery_code_id)
            .values(attempts=RecoveryCode.attempts + 1)
        )
        await self._db.commit()

    async def get_by_user_id(self, user_id: UUID) -> RecoveryCode | None:
        result = await self._db.execute(
            select(RecoveryCode)
            .where(
                RecoveryCode.user_id == user_id,
                RecoveryCode.used_at.is_(None),
                RecoveryCode.expires_at > datetime.now(timezone.utc)
            )
        )

        return result.scalar_one_or_none()
