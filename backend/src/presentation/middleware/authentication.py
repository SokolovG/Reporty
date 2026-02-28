from logging import getLogger

from litestar import Litestar
from litestar.connection import ASGIConnection
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult
from litestar.types import ASGIApp

from backend.src.infrastructure.exceptions.api_exceptions import AuthenticationError
from backend.src.application.ports.repositories import IUserRepository
from backend.src.infrastructure.encryption.jwt_service import JWTService

logger = getLogger(__name__)


class JWTAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    def __init__(self, app: ASGIApp):
        exclude = [
            "/api/v1/auth/register",
            "/api/v1/auth/login",
            "/api/v1/auth/refresh",
            "/admin/*",
            "/schema/*",
            "/docs/*",
        ]
        super().__init__(app, exclude=exclude)

    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:
        app = Litestar.from_scope(connection.scope)
        container = app.state.dishka_container

        access_token = connection.cookies.get("accessToken")

        if not access_token:
            auth_header = connection.headers.get("authorization")
            if auth_header and auth_header.startswith("Bearer "):
                access_token = auth_header[7:]  # delete "Bearer "

        if not access_token:
            raise AuthenticationError("No access token")

        async with container() as request_container:
            jwt_service = await request_container.get(JWTService)
            user_repo = await request_container.get(IUserRepository)

            payload = await jwt_service.verify_token(access_token)
            if not payload:
                raise AuthenticationError("Invalid token")

            user = await user_repo.get_one_or_none(id=int(payload["sub"]))
            if not user:
                raise AuthenticationError("User not found")

        return AuthenticationResult(user=user, auth=access_token)
