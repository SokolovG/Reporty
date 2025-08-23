from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult
from litestar.connection import ASGIConnection
from litestar.types import ASGIApp
from backend.src.core.exceptions import AuthenticationError
from backend.src.services import JWTService
from backend.src.database.repositories import UserRepository


class JWTAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    def __init__(self, app: ASGIApp, jwt_service: JWTService, user_repo: UserRepository):
        exclude = ["/api/v1/auth/*", "/admin/*", "/docs", "/schema"]
        super().__init__(app, exclude=exclude)
        self.jwt_service = jwt_service
        self.user_repo = user_repo

    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:
        access_token = connection.cookies.get("access_token")
        if not access_token:
            raise AuthenticationError("No access token")

        payload = await self.jwt_service.verify_token(access_token)
        if not payload:
            raise AuthenticationError("Invalid token")

        user = await self.user_repo.get(payload["sub"])
        return AuthenticationResult(user=user, auth=access_token)
