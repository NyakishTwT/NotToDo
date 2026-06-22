from typing import Any
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .interfaces import UsersServiceABC, UsersRepoABC


class UsersService(UsersServiceABC):
    users_repo: UsersRepoABC

    async def create_user(self, session: AsyncSession, email: str, name: str) -> Any:
        existing_user = await self.users_repo.get_by_email(session, email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует",
            )

        if not name.strip():
            raise ValueError("Имя пользователя не может быть пустым")

        return await self.users_repo.create(session, email, name)

    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> Any:
        user = await self.users_repo.get_by_id(session, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с id {user_id} не найден",
            )
        return user
