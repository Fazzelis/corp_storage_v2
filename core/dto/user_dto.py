from dataclasses import dataclass


@dataclass
class PasswordChangedDto:
    message: str

@dataclass
class UserDto:
    email: str
    name: str
    surname: str
    patronymic: str | None
    avatar_path: str | None
    must_change_password: bool
