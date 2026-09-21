from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from uuid import uuid4
from database.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(16), nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    surname: Mapped[str] = mapped_column(String(256), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(256))
    avatar_path: Mapped[str] = mapped_column(String())
