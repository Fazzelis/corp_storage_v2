from database.database import Base
from core.enums.refresh_token_status_enum import RefreshTokenStatusEnum

from uuid import UUID, uuid4
from sqlalchemy import Uuid, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
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
    rotated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
