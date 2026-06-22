from typing import Any
from fastapi import APIRouter, Query, Path, status
from web_fractal.db import serialize

from .dtos import TodoCreate
from .interfaces import TodosControllerABC, TodosServiceABC
from .dms import TodoDM


class TodosController(TodosControllerABC):
    router = APIRouter(prefix="/todos", tags=["todos"])

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
        todos = await self.todos_service.get_user_todos(user_id=user_id)
        return serialize(TodoDM, todos, as_list=True)

    async def create_todo(self, data: TodoCreate) -> Any:
        result = await self.todos_service.add_todo(
            title=data.title, user_id=data.user_id
        )
        return serialize(TodoDM, result, as_list=False)

    async def complete_todo(self, id: int = Path(...)) -> Any:
        result = await self.todos_service.complete_todo(todo_id=id)
        return serialize(TodoDM, result, as_list=False)
