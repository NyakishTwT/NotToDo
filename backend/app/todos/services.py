from typing import Any
from sqlalchemy.ext.asyncio import async_sessionmaker
from web_fractal.db import UnitOfWork

from app.users.interfaces import UsersServiceABC
from .interfaces import TodosServiceABC, TodosRepoABC


class TodosService(TodosServiceABC):
    todos_repo: TodosRepoABC
    users_service: UsersServiceABC
    session_maker: async_sessionmaker

    async def get_user_todos(self, user_id: int) -> list[Any]:
        await self.users_service.get_user_by_id(user_id)
        return await self.todos_repo.get_all_by_user(user_id)

    async def add_todo(self, title: str, user_id: int) -> Any:
        if not title.strip():
            raise ValueError("Название задачи не может быть пустым")

        async with UnitOfWork(self.session_maker) as uow:
            await self.users_service.get_user_by_id(user_id, uow=uow)
            return await self.todos_repo.create(title, user_id, uow=uow)

    async def complete_todo(self, todo_id: int):
        async with UnitOfWork(self.session_maker) as uow:
            todo = await self.todos_repo.get_by_id(todo_id, uow=uow)
            if todo:
                todo.is_done = True
                session = uow.get_session()
                await session.flush()
                await session.refresh(todo)
            return todo
