from database.database import Base

from uuid import UUID, uuid4
from sqlalchemy import Uuid, Enum, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

class RecoveryCode(Base):
    __tablename__ = "recovery_code"
    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=lambda: uuid4())
    code: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="recovery_codes")
