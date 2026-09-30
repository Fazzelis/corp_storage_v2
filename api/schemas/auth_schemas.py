from pydantic import BaseModel


class UserRegistrateResponse(BaseModel):
    id: str
    email: str
