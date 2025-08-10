from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get, post, Request

from backend.src.api.dto import (
    ChangePasswordRequest,
    RefreshTokenRequest,
    LogoutRequest,
    LoginRequest,
    RegisterRequest,
)
from backend.src.api.decorators import auth_error_handler
from backend.src.api.dto.auth_dto import (
    UserResponse,
    SuccessLoginResponse,
    SuccessLogoutResponse,
    SuccessRefreshResponse,
    SuccessChangePasswordResponse,
)
from backend.src.api.responses import ErrorResponse
from backend.src.services import AuthService


class AuthController(Controller):
    @post("/register")
    @auth_error_handler
    @inject
    async def register(
        self, service: FromDishka[AuthService], request: Request, data: RegisterRequest
    ) -> UserResponse | ErrorResponse:
        return await service.register(data)

    @post("/login")
    @auth_error_handler
    @inject
    async def login(
        self, service: FromDishka[AuthService], request: Request, data: LoginRequest
    ) -> SuccessLoginResponse | ErrorResponse:
        return await service.login(data)

    @post("/logout")
    @auth_error_handler
    @inject
    async def logout(
        self, service: FromDishka[AuthService], request: Request, data: LogoutRequest
    ) -> SuccessLogoutResponse | ErrorResponse:
        return await service.logout(data)

    @post("/refresh")
    @auth_error_handler
    @inject
    async def refresh_token(
        self, service: FromDishka[AuthService], request: Request, data: RefreshTokenRequest
    ) -> SuccessRefreshResponse | ErrorResponse:
        return await service.refresh(data)

    @post("/change-password")
    @auth_error_handler
    @inject
    async def change_password(
        self, service: FromDishka[AuthService], request: Request, data: ChangePasswordRequest
    ) -> SuccessChangePasswordResponse | ErrorResponse:
        return await service.change_password(data)

    @get("/me")
    @auth_error_handler
    @inject
    async def get_me(
        self,
        service: FromDishka[AuthService],
        request: Request,
    ) -> UserResponse | ErrorResponse:
        return await service.get_me()
