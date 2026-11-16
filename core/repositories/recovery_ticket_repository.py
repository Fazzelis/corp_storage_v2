from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from core.models.recovery_ticket import RecoveryTicket
from datetime import datetime, timezone, timedelta

from configuration import settings

class RecoveryTicketRepository:
    def __init__(self, db: AsyncSession):
        self._db: AsyncSession = db

    async def post(
            self,
            user_id: UUID,
            ticket_hash: str
    ) -> RecoveryTicket:
        created_at = datetime.now(timezone.utc)
        expires_at = created_at + timedelta(minutes=settings.recovery_ticket_ttl)
        ticket_db = RecoveryTicket(
            ticket=ticket_hash,
            created_at=created_at,
            expires_at=expires_at,
            user_id=user_id
        )
        self._db.add(ticket_db)
        await self._db.commit()
        await self._db.refresh(ticket_db)
        return ticket_db

    async def get_by_user_id(self, user_id: UUID) -> RecoveryTicket | None:
        result = await self._db.execute(
            select(RecoveryTicket)
            .where(
                RecoveryTicket.user_id == user_id,
                RecoveryTicket.used_at.is_(None),
                RecoveryTicket.expires_at > datetime.now(timezone.utc)
            )
        )

        return result.scalar_one_or_none()

    async def get_by_hash(self, ticket_hash: str) -> RecoveryTicket | None:
        result = await self._db.execute(
            select(RecoveryTicket)
            .where(
                RecoveryTicket.ticket == ticket_hash,
                RecoveryTicket.expires_at > datetime.now(timezone.utc),
                RecoveryTicket.used_at.is_(None)
            )
        )

        return result.scalar_one_or_none()

    async def invalidate(self, recovery_ticket_id: UUID):
        await self._db.execute(
            update(RecoveryTicket)
            .where(
                RecoveryTicket.id == recovery_ticket_id,
                RecoveryTicket.expires_at > datetime.now(timezone.utc)
            )
            .values(used_at=datetime.now(timezone.utc))
        )
        await self._db.commit()
