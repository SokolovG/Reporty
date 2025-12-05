from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.repositories.auth.user_repository import UserRepository
from backend.src.services.auth.jwt_service import JWTService
from backend.src.core.configs import get_sqlalchemy_config


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str) -> None:
        super().__init__(secret_key)

    async def _get_session(self) -> AsyncSession:
        """Get database session."""
        sqlalchemy_config = get_sqlalchemy_config()
        session_maker = sqlalchemy_config.create_session_maker()
        return session_maker()

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        if not email or not password:
            return False

        async with await self._get_session() as session:
            user_repo = UserRepository(session=session)
            jwt_service = JWTService()

            user = await user_repo.get_one_or_none(email=email)
            if not user:
                return False
            if not user.is_admin:
                return False

            success = await jwt_service.verify_password(password, user.password_hash)  # type: ignore
            if not success:
                return False

            request.session["user_id"] = user.id
            request.session["is_admin"] = True
            return True

    async def authenticate(self, request: Request) -> bool:
        user_id = request.session.get("user_id")
        is_admin = request.session.get("is_admin")

        if user_id and is_admin:
            async with await self._get_session() as session:
                user_repo = UserRepository(session=session)
                user = await user_repo.get_one_or_none(id=user_id)

                if user and user.is_admin:
                    return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
