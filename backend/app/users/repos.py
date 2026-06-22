from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from web_fractal.db import UnitOfWork

from .interfaces import UsersRepoABC
from .models import UserORM


class UsersRepo(UsersRepoABC):
    session_maker: async_sessionmaker

    async def create(
        self, email: str, name: str, uow: UnitOfWork | None = None
    ) -> UserORM:
        if uow:
            session = uow.get_session()
            new_user = UserORM(email=email, name=name)
            session.add(new_user)
            await session.flush()
            return new_user

        async with UnitOfWork(self.session_maker) as local_uow:
            session = local_uow.get_session()
            new_user = UserORM(email=email, name=name)
            session.add(new_user)
            await session.flush()
            await session.refresh(new_user)
            return new_user

    async def get_by_id(
        self, user_id: int, uow: UnitOfWork | None = None
    ) -> UserORM | None:
        query = select(UserORM).where(UserORM.id == user_id)
        if uow:
            return await uow.get_session().scalar(query)

        async with UnitOfWork(self.session_maker) as local_uow:
            return await local_uow.get_session().scalar(query)

    async def get_by_email(
        self, email: str, uow: UnitOfWork | None = None
    ) -> UserORM | None:
        query = select(UserORM).where(UserORM.email == email)
        if uow:
            return await uow.get_session().scalar(query)

        async with UnitOfWork(self.session_maker) as local_uow:
            return await local_uow.get_session().scalar(query)
