from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend

from backend.src.core.exceptions import AuthenticationError
from backend.src.services.jwt_service import JWTService

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str) -> None:
        self.jwt_service = JWTService()

        self.middlewares = [
            Middleware(SessionMiddleware, secret_key=secret_key),
        ]

    async def login(self, request: Request) -> bool: ...

    async def authenticate(self, request: Request) -> bool:
        token = request.cookies.get("accessToken")
        if not token:
            return False

        try:
            payload = await self.jwt_service.verify_token(token)
            user_id = int(payload["sub"])
            # TODO: add role verification via UserRepository
            return True
        except AuthenticationError:
            return False

    # TODO: add new endpoint only for adding admin with flag is_admin true default

    async def logout(request) -> bool: ...
