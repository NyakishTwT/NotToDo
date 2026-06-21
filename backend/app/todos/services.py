from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from .interfaces import TodosServiceABC, TodosRepoABC


class TodosService(TodosServiceABC):
    todos_repo: TodosRepoABC

    async def get_user_todos(self, session: AsyncSession, user_id: int) -> list[Any]:
        return await self.todos_repo.get_all_by_user(session, user_id)

    async def add_todo(self, session: AsyncSession, title: str, user_id: int) -> Any:
        if not title.strip():
            raise ValueError("Название задачи не может быть пустым")
        return await self.todos_repo.create(session, title, user_id)
