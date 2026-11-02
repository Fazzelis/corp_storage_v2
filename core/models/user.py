from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Uuid
from uuid import uuid4
from database.database import Base
from uuid import UUID


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=lambda: uuid4())
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    surname: Mapped[str] = mapped_column(String(256), nullable=False)
    patronymic: Mapped[str | None] = mapped_column(String(256), nullable=True)
    avatar_path: Mapped[str | None] = mapped_column(String(), nullable=True)
