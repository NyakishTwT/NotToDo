from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from web_fractal.db import UnitOfWork

from .interfaces import TodosRepoABC
from .models import TodoORM


class TodosRepo(TodosRepoABC):
    session_maker: async_sessionmaker

    async def get_all_by_user(
        self, user_id: int, uow: UnitOfWork | None = None
    ) -> list[TodoORM]:
        query = select(TodoORM).where(TodoORM.user_id == user_id)
        if uow:
            result = await uow.get_session().scalars(query)
            return list(result.all())

        async with UnitOfWork(self.session_maker) as local_uow:
            result = await local_uow.get_session().scalars(query)
            return list(result.all())

    async def create(
        self, title: str, user_id: int, uow: UnitOfWork | None = None
    ) -> TodoORM:
        if uow:
            session = uow.get_session()
            new_todo = TodoORM(title=title, user_id=user_id)
            session.add(new_todo)
            await session.flush()
            return new_todo

        async with UnitOfWork(self.session_maker) as local_uow:
            session = local_uow.get_session()
            new_todo = TodoORM(title=title, user_id=user_id)
            session.add(new_todo)
            await session.flush()
            await session.refresh(new_todo)
            return new_todo

    async def get_by_id(
        self, todo_id: int, uow: UnitOfWork | None = None
    ) -> TodoORM | None:
        query = select(TodoORM).where(TodoORM.id == todo_id)
        if uow:
            return await uow.get_session().scalar(query)

        async with UnitOfWork(self.session_maker) as local_uow:
            return await local_uow.get_session().scalar(query)
