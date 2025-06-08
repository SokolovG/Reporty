from typing import Any

from litestar import Request
from litestar_users.service import BaseUserService

from backend.src.database.models import User


class UserService(BaseUserService[User, Any, Any]):  # type: ignore
    async def post_registration_hook(self, user: User, request: Request) -> None:  # type: ignore
        """Hook called after successful user registration."""  # noqa: D401
        print(f"User <{user.email}> has registered!")
        # - отправка welcome email
        # - создание профиля пользователя
        # - логирование события
