from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from core.enums.user_role_enum import UserRoleEnum


@dataclass
class SuccessfulUserRegistration:
    id: UUID
    email: str
    name: str
    surname: str
    patronymic: str | None = None
    avatar_path: str | None = None


@dataclass
class SuccessfulUserLogin:
    id: UUID
    email: str
    name: str
    surname: str
    access_token: str
    refresh_token: str
    must_change_password: bool
    role: UserRoleEnum
    patronymic: str | None = None
    avatar_path: str | None = None


@dataclass
class SuccessfulRefresh:
    access_token: str
    refresh_token: str


@dataclass
class ResendAtRecoveryCodeDto:
    can_resend_at: int


@dataclass
class RecoveryTicketDto:
    recovery_ticket: str
    expires_at: datetime
