# app/todos/controllers.py
from typing import Any
from fastapi import APIRouter, Query, status
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from web_fractal.db import UnitOfWork, serialize


from .dtos import TodoCreate
from .interfaces import TodosControllerABC, TodosServiceABC
from .dms import TodoDM


class TodosController(TodosControllerABC):
    router = APIRouter(prefix="/todos", tags=["todos"])

    session_maker: async_sessionmaker
    todos_service: TodosServiceABC

    def init_http_routes(self) -> None:
        self.reg_route(self.get_todos, methods=["GET"], path="")
        self.reg_route(
            self.create_todo,
            methods=["POST"],
            path="",
            status_code=status.HTTP_201_CREATED,
        )

    async def get_todos(self, user_id: int = Query(...)) -> list[Any]:
        async with UnitOfWork(self.session_maker) as uow:
            session = uow.get_session()
            todos = await self.todos_service.get_user_todos(session, user_id)
            return serialize(TodoDM, todos, as_list=True)

    async def create_todo(self, data: TodoCreate) -> Any:
        async with UnitOfWork(self.session_maker) as uow:
            session = uow.get_session()
            result = await self.todos_service.add_todo(
                session, data.title, data.user_id
            )
            await session.commit()
            return serialize(TodoDM, result, as_list=False)
