from dataclasses import dataclass


@dataclass
class SuccessfulUserRegistration:
    id: str
    email: str


@dataclass
class SuccessfulUserLogin:
    id: str
    email: str
    name: str
    surname: str
    patronymic: str | None = None
    avatar_path: str | None = None
