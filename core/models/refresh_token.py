from database.database import Base
from core.enums.refresh_token_status_enum import RefreshTokenStatusEnum

from uuid import UUID, uuid4
from sqlalchemy import Uuid, Enum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=lambda: uuid4())
    jti: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    family_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    status: Mapped[RefreshTokenStatusEnum] = mapped_column(
        Enum(RefreshTokenStatusEnum, name="refresh_token_status_enum"),
        default=RefreshTokenStatusEnum.REVOKED,
        nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    rotated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")
