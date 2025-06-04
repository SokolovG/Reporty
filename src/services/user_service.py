from typing import Any

from litestar_users.service import BaseUserService

from src.database.models import User


class UserService(BaseUserService[User, Any, Any]):  # type:ignore
    async def post_registration_hook(self, user: User) -> None:  # type:ignore
        print(f"User <{user.email}> has registered!")
