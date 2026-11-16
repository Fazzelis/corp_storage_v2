from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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
