from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .interfaces import UsersRepoABC
from .models import UserORM


class UsersRepo(UsersRepoABC):
    async def create(self, session: AsyncSession, email: str, name: str) -> UserORM:
        new_user = UserORM(email=email, name=name)
        session.add(new_user)
        await session.flush()
        return new_user

    async def get_by_id(self, session: AsyncSession, user_id: int) -> UserORM | None:
        query = select(UserORM).where(UserORM.id == user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, session: AsyncSession, email: str) -> UserORM | None:
        query = select(UserORM).where(UserORM.email == email)
        result = await session.execute(query)
        return result.scalar_one_or_none()
