from pydantic import BaseModel
from pydantic import EmailStr

class RegistrateRequest(BaseModel):
    email: EmailStr
    name: str
    surname: str
    patronymic: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenInfoResponse(BaseModel):
    token: str
    type: str


class LoginResponse(BaseModel):
    token: TokenInfoResponse
    role: str


class SendRecoveryCodeRequest(BaseModel):
    email: EmailStr

class SendRecoveryCodeResponse(BaseModel):
    time_for_resend: int


class VerifyRecoveryCodeRequest(BaseModel):
    email: EmailStr
    recovery_code: str


class VerifyRecoveryCodeResponse(BaseModel):
    recovery_ticket: str


class ChangePasswordRequest(BaseModel):
    recovery_ticket: str
    new_password: str


class ChangePasswordResponse(BaseModel):
    message: str
