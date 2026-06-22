from archtool.layers.default_layer_interfaces import ABCController, ABCRepo, ABCService
from abc import abstractmethod
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from web_fractal.http.interfaces import HttpControllerABC

from .dtos import TodoCreate


# Возврат с типом Any может будут заменены на типобезопасное поведение, с помощью тех же dto
# ------ Repo ------
class TodosRepoABC(ABCRepo):
    @abstractmethod
    async def get_all_by_user(self, session: AsyncSession, user_id: int) -> list[Any]:
        """Получить все задачи пользователя"""
        ...

    @abstractmethod
    async def create(self, session: AsyncSession, title: str, user_id: int) -> Any:
        """Создать новую задачку"""
        ...

    @abstractmethod
    async def get_by_id(self, session: AsyncSession, todo_id: int) -> Any | None:
        """Найти задачу по её уникальному ID"""
        ...


# ------ Services ------
class TodosServiceABC(ABCService):
    @abstractmethod
    async def get_user_todos(self, session: AsyncSession, user_id: int) -> list[Any]:
        """Домейн логика получения задач"""
        ...

    @abstractmethod
    async def add_todo(self, session: AsyncSession, title: str, user_id: int) -> Any:
        """Домейн логика создания задачи"""
        ...

    @abstractmethod
    async def complete_todo(self, session: AsyncSession, todo_id: int) -> Any:
        ...
        """Домейн логика для выполненного или не выполненного todo"""


# ------ Controllers ------
class TodosControllerABC(ABCController, HttpControllerABC):
    @abstractmethod
    async def get_todos(self, user_id: int) -> list[Any]:
        """Эндпоинт для получения todo"""
        ...

    @abstractmethod
    async def create_todo(self, data: TodoCreate) -> Any:
        """Эндпоинт для поста todo"""
        ...

    @abstractmethod
    async def complete_todo(self, id: int) -> Any:
        """Эндпоинт патч для todo(Done or not done)"""
        ...
