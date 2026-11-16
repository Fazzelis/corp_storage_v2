from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Uuid, Boolean, Enum
from uuid import uuid4

from core.enums.user_role_enum import UserRoleEnum
from database.database import Base
from uuid import UUID


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=lambda: uuid4())
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    surname: Mapped[str] = mapped_column(String(256), nullable=False)
    patronymic: Mapped[str | None] = mapped_column(String(256), nullable=True)
    avatar_path: Mapped[str | None] = mapped_column(String(), nullable=True)
    must_change_password: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum, name="user_role"),
        default=UserRoleEnum.EMPLOYER,
        nullable=False
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    recovery_codes: Mapped[list["RecoveryCode"]] = relationship(
        "RecoveryCode",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    recovery_tickets: Mapped[list["RecoveryTicket"]] = relationship(
        "RecoveryTicket",
        back_populates="user",
        cascade="all, delete-orphan"
    )
