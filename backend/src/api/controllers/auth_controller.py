from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get, Request

from backend.src.api.dto import (
    UserReadDTO,
    ChangePasswordRequest,
    RefreshTokenRequest,
    LogoutRequest,
    LoginRequest,
    RegisterRequest,
)
from backend.src.api.dto.user_dto import UserReadSchema
from backend.src.services import AuthService


class AuthController(Controller):
    @inject
    async def register(
        self, service: FromDishka[AuthService], request: Request, data: RegisterRequest
    ) -> None:
        result = await service.register(data)  # type: ignore
        return None

    @inject
    async def login(
        self, service: FromDishka[AuthService], request: Request, data: LoginRequest
    ) -> None:
        result = await service.login(data)  # type: ignore
        return None

    @inject
    async def logout(
        self, service: FromDishka[AuthService], request: Request, data: LogoutRequest
    ) -> None:
        result = await service.logout(data)  # type: ignore
        return None

    @inject
    async def refresh(
        self, service: FromDishka[AuthService], request: Request, data: RefreshTokenRequest
    ) -> None:
        result = await service.refresh(data)  # type: ignore
        return None

    @inject
    async def change_password(
        self, service: FromDishka[AuthService], request: Request, data: ChangePasswordRequest
    ) -> None:
        result = await service.change_password(data)  # type: ignore
        return None

    @get("/me", return_dto=UserReadDTO)
    @inject
    async def get_me(
        self,
        service: FromDishka[AuthService],
        request: Request,
    ) -> UserReadSchema:
        user = await service.get_me()
        return user  # type: ignore
