from typing import Any
from fastapi import APIRouter, Path, status
from web_fractal.db import serialize

from .dtos import UserCreate
from .dms import UserDM
from .interfaces import UsersControllerABC, UsersServiceABC


class UsersController(UsersControllerABC):
    router = APIRouter(prefix="/users", tags=["users"])

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
        result = await self.users_service.create_user(email=data.email, name=data.name)
        return serialize(UserDM, result, as_list=False)

    async def get_user(self, id: int = Path(...)) -> Any:
        user = await self.users_service.get_user_by_id(user_id=id)
        return serialize(UserDM, user, as_list=False)
