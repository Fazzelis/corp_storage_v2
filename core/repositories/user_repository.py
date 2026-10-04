from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.user import User


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def get_by_email(self, email: str) -> User | None:
        result = await self._db_session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def post(
            self,
            email: str,
            password: str,
            name: str,
            surname: str,
            patronymic: str | None
    ) -> User:
        new_user = User(
            email=email,
            password=password,
            name=name,
            surname=surname,
            patronymic=patronymic
        )

        self._db_session.add(new_user)
        await self._db_session.commit()
        await self._db_session.refresh(new_user)
        return new_user
