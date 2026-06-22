from typing import Any
from fastapi import APIRouter, Query, Path, status
from web_fractal.db import serialize, UnitOfWork
from sqlalchemy.ext.asyncio import async_sessionmaker

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
        self.reg_route(self.complete_todo, methods=["PATCH"], path="/{id}/complete")

    async def get_todos(self, user_id: int = Query(...)) -> list[Any]:
        async with UnitOfWork(self.session_maker) as uow:
            session = uow.get_session()
            todos = await self.todos_service.get_user_todos(session, user_id=user_id)
            return serialize(TodoDM, todos, as_list=True)

    async def create_todo(self, data: TodoCreate) -> Any:
        async with UnitOfWork(self.session_maker) as uow:
            session = uow.get_session()
            result = await self.todos_service.add_todo(
                session, title=data.title, user_id=data.user_id
            )
            await session.commit()
            return serialize(TodoDM, result, as_list=False)

    async def complete_todo(self, id: int = Path(...)) -> Any:
        async with UnitOfWork(self.session_maker) as uow:
            session = uow.get_session()
            result = await self.todos_service.complete_todo(session, todo_id=id)
            await session.commit()
            await session.refresh(result)
            return serialize(TodoDM, result, as_list=False)
