from typing import Any
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .interfaces import UsersServiceABC, UsersRepoABC


class UsersService(UsersServiceABC):
    users_repo: UsersRepoABC

    async def create_user(self, session: AsyncSession, email: str, name: str) -> Any:
        if not name.strip():
            raise ValueError("Имя не может быть пустым")
        existing = await self.users_repo.get_by_email(session, email)
        if existing:
            raise HTTPException(400, "Пользователь с таким email уже существует")
        return await self.users_repo.create(session, email, name)

    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> Any:
        user = await self.users_repo.get_by_id(session, user_id)
        if not user:
            raise HTTPException(404, f"Пользователь с id {user_id} не найден")
        return user
