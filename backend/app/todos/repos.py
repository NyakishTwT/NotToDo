from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .interfaces import TodosRepoABC
from .models import TodoORM


class TodosRepo(TodosRepoABC):
    async def get_all_by_user(
        self, session: AsyncSession, user_id: int
    ) -> list[TodoORM]:
        query = select(TodoORM).where(TodoORM.user_id == user_id)
        result = await session.execute(query)
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, title: str, user_id: int) -> TodoORM:
        new_todo = TodoORM(title=title, user_id=user_id)
        session.add(new_todo)
        await session.flush()
        return new_todo

    async def get_by_id(self, session: AsyncSession, todo_id: int) -> TodoORM | None:
        query = select(TodoORM).where(TodoORM.id == todo_id)
        return await session.scalar(query)
