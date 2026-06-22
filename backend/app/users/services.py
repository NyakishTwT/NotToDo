from typing import Any
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import async_sessionmaker
from web_fractal.db import UnitOfWork

from .interfaces import UsersServiceABC, UsersRepoABC


class UsersService(UsersServiceABC):
    users_repo: UsersRepoABC
    session_maker: async_sessionmaker

    async def create_user(self, email: str, name: str) -> Any:
        if not name.strip():
            raise ValueError("Имя пользователя не может быть пустым")

        async with UnitOfWork(self.session_maker) as uow:
            existing_user = await self.users_repo.get_by_email(email, uow=uow)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Пользователь с таким email уже существует",
                )

            return await self.users_repo.create(email, name, uow=uow)

    async def get_user_by_id(self, user_id: int, uow: UnitOfWork | None = None) -> Any:
        user = await self.users_repo.get_by_id(user_id, uow=uow)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с id {user_id} не найден",
            )
        return user
