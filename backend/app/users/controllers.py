from typing import Any
from fastapi import APIRouter, Path, status
from sqlalchemy.ext.asyncio import async_sessionmaker
from web_fractal.db import UnitOfWork, serialize

from .dtos import UserCreate
from .dms import UserDM
from .interfaces import UsersControllerABC, UsersServiceABC


class UsersController(UsersControllerABC):
    router = APIRouter(prefix="/users", tags=["users"])

    session_maker: async_sessionmaker
    users_service: UsersServiceABC

    def init_http_routes(self) -> None:
        self.reg_route(
            self.create_user,
            methods=["POST"],
            path="",
            status_code=status.HTTP_201_CREATED,
        )
        self.reg_route(self.get_user, methods=["GET"], path="/{id}")

    async def create_user(self, data: UserCreate) -> Any:
        async with UnitOfWork(self.session_maker) as uow:
            session = uow.get_session()
            result = await self.users_service.create_user(
                session, data.email, data.name
            )
            await session.commit()
            return serialize(UserDM, result, as_list=False)

    async def get_user(self, id: int = Path(...)) -> Any:
        async with UnitOfWork(self.session_maker) as uow:
            session = uow.get_session()
            user = await self.users_service.get_user_by_id(session, id)
            return serialize(UserDM, user, as_list=False)
