from archtool.layers.default_layer_interfaces import ABCController, ABCRepo, ABCService
from abc import abstractmethod
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from web_fractal.http.interfaces import HttpControllerABC

from .dtos import UserCreate


# ------ Repo ------
class UsersRepoABC(ABCRepo):
    @abstractmethod
    async def create(self, session: AsyncSession, email: str, name: str) -> Any:
        """Создать пользователя в БД"""
        ...

    @abstractmethod
    async def get_by_id(self, session: AsyncSession, user_id: int) -> Any | None:
        """Получить пользователя по ID"""
        ...

    @abstractmethod
    async def get_by_email(self, session: AsyncSession, email: str) -> Any | None:
        """Проверить существование email"""
        ...


# ------ Services ------
class UsersServiceABC(ABCService):
    @abstractmethod
    async def create_user(self, session: AsyncSession, email: str, name: str) -> Any:
        """Бизнес-логика создания пользователя"""
        ...

    @abstractmethod
    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> Any:
        """Бизнес-логика получения пользователя"""
        ...


# ------ Controllers ------
class UsersControllerABC(ABCController, HttpControllerABC):
    @abstractmethod
    async def create_user(self, data: UserCreate) -> Any:
        """Эндпоинт создать юзера"""
        ...

    @abstractmethod
    async def get_user(self, id: int) -> Any:
        """Эндпоинт взять юзера"""
        ...
