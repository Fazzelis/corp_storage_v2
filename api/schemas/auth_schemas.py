from pydantic import BaseModel
from datetime import datetime


class RegistrateRequest(BaseModel):
    email: str
    name: str
    surname: str
    patronymic: str | None = None


class RegistrateResponse(BaseModel):
    id: str
    email: str
    name: str
    surname: str
    patronymic: str | None
    avatar_path: str | None


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenInfoResponse(BaseModel):
    token: str
    type: str


class LoginResponse(BaseModel):
    id: str
    email: str
    name: str
    surname: str
    token: TokenInfoResponse
    must_change_password: bool
    patronymic: str | None = None
    avatar_path: str | None = None


class SendRecoveryCodeRequest(BaseModel):
    email: str

class SendRecoveryCodeResponse(BaseModel):
    message: str


class VerifyRecoveryCodeRequest(BaseModel):
    email: str
    recovery_code: str


class VerifyRecoveryCodeResponse(BaseModel):
    recovery_ticket: str
    expires_at: datetime
