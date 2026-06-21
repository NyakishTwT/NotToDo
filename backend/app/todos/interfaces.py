from archtool.layers.default_layer_interfaces import ABCController, ABCRepo, ABCService
from abc import abstractmethod
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from web_fractal.http.interfaces import HttpControllerABC


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


# ------ Services ------
class TodosServiceABC(ABCService):
    @abstractmethod
    async def get_user_todos(self, session: AsyncSession, user_id: int) -> list[Any]:
        """Домейн логика получения задач"""

    @abstractmethod
    async def add_todo(self, session: AsyncSession, title: str, user_id: int) -> Any:
        """Домейн логика создания задачи"""


# ------ Controllers ------
class TodosControllerABC(ABCController, HttpControllerABC):
    @abstractmethod
    async def get_todos(self) -> list[Any]:
        """Эндпоинт для получения списка todo"""

    @abstractmethod
    async def create_todo(self) -> Any:
        """Эндпоинт для создания todo"""
