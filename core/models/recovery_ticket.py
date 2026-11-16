from database.database import Base

from uuid import UUID, uuid4
from sqlalchemy import Uuid, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class RecoveryTicket(Base):
    __tablename__ = "recovery_ticket"
    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=lambda: uuid4())
    ticket: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="recovery_tickets")
