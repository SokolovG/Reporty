from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get, post, Request, Response

from backend.src.api.dto import (
    ChangePasswordRequest,
    RefreshTokenRequest,
    LoginRequest,
    RegisterRequest,
)
from backend.src.api.decorators import auth_error_handler
from backend.src.api.responses import ErrorResponse, SuccessResponse
from backend.src.services import AuthService
from backend.src.api.dto import SuccessResponseDTO

class AuthController(Controller):
    @post("/register", return_dto=SuccessResponseDTO)
    @auth_error_handler
    @inject
    async def register(
        self, service: FromDishka[AuthService], request: Request, data: RegisterRequest
    ) -> SuccessResponse | ErrorResponse:
        return await service.register(data)

    @post("/login")
    @auth_error_handler
    @inject
    async def login(
        self, service: FromDishka[AuthService], response: Response, data: LoginRequest
    ) -> SuccessResponse | ErrorResponse:
        result = await service.login(data)
        if isinstance(result, SuccessResponse):
            refresh_token = result.data.get("refresh")
            if refresh_token:
                response.set_cookie(
                    "refresh_token",
                    refresh_token,
                    httponly=True,
                    secure=True,
                    samesite="strict",
                    max_age=7 * 24 * 60 * 60,
                )
        return result

    @post("/logout")
    @auth_error_handler
    @inject
    async def logout(self, response: Response) -> SuccessResponse:
        from backend.src.api.utils.success_utils import logout_success

        response.delete_cookie(key="refresh_token")
        return logout_success()

    @post("/refresh")
    @auth_error_handler
    @inject
    async def refresh_token(
        self, service: FromDishka[AuthService], request: Request, data: RefreshTokenRequest
    ) -> SuccessResponse | ErrorResponse:
        return await service.refresh(data)

    @post("/change-password")
    @auth_error_handler
    @inject
    async def change_password(
        self, service: FromDishka[AuthService], request: Request, data: ChangePasswordRequest
    ) -> SuccessResponse | ErrorResponse:
        return await service.change_password(data)

    @get("/me")
    @auth_error_handler
    @inject
    async def get_me(
        self,
        service: FromDishka[AuthService],
        request: Request,
    ) -> SuccessResponse | ErrorResponse:
        return await service.get_me()
