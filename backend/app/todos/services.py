from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.interfaces import UsersServiceABC
from .interfaces import TodosServiceABC, TodosRepoABC


class TodosService(TodosServiceABC):
    todos_repo: TodosRepoABC
    users_service: UsersServiceABC

    async def get_user_todos(self, session: AsyncSession, user_id: int) -> list[Any]:
        await self.users_service.get_user_by_id(session, user_id)
        return await self.todos_repo.get_all_by_user(session, user_id)

    async def add_todo(self, session: AsyncSession, title: str, user_id: int) -> Any:
        if not title.strip():
            raise ValueError("Название задачи не может быть пустым")
        await self.users_service.get_user_by_id(session, user_id)
        return await self.todos_repo.create(session, title, user_id)

    async def complete_todo(self, session: AsyncSession, todo_id: int):
        todo = await self.todos_repo.get_by_id(session, todo_id)
        if todo:
            todo.is_done = True
            await session.flush()
            await session.refresh(todo)
        return todo
