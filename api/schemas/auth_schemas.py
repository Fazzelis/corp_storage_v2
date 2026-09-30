from pydantic import BaseModel


class UserRegistrateResponse(BaseModel):
    id: str
    email: str


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
