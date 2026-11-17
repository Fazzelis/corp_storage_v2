from pydantic import BaseModel, ConfigDict


class ChangeProfileInfoRequest(BaseModel):
    email: str | None = None
    name: str | None = None
    surname: str | None = None
    patronymic: str | None = None


class UserInfoResponse(BaseModel):
    email: str
    name: str
    surname: str
    patronymic: str | None
    avatar_path: str | None
    must_change_password: bool

    model_config = ConfigDict(from_attributes=True)
