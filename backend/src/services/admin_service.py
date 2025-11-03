from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend

from backend.src.core.dependencies import get_dependency
from backend.src.database.repositories.user_repository import UserRepository
from backend.src.services.jwt_service import JWTService


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str) -> None:
        super().__init__(secret_key)

    async def login(self, request: Request) -> bool:
        jwt_service = await get_dependency(request, JWTService)
        user_repo = await get_dependency(request, UserRepository)

        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        if not email or not password:
            return False

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
            user_repo = await get_dependency(request, UserRepository)
            user = await user_repo.get_one_or_none(id=user_id)

            if user and user.is_admin:
                return True

        return False

    # TODO: add new endpoint only for adding admin with flag is_admin true default(OR?)

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
