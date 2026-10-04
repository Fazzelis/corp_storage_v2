from pydantic import BaseModel


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


class LoginResponse(BaseModel):
    id: str
    email: str
    name: str
    surname: str
    patronymic: str | None = None
    avatar_path: str | None = None
