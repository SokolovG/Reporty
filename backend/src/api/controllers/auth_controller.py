from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get, post, Request, Response

from backend.src.api.dto import (
    ChangePasswordRequest,
    RefreshTokenRequest,
    LoginRequest,
    RegisterRequest,
)
from backend.src.api.responses.base_responses import SuccessResponse
from backend.src.services import AuthService
from backend.src.api.dto import SuccessResponseDTO


class AuthController(Controller):
    @post("/register", return_dto=SuccessResponseDTO)
    @inject
    async def register(
        self, service: FromDishka[AuthService], request: Request, data: RegisterRequest
    ) -> SuccessResponse:
        result = await service.register(data)
        return SuccessResponse(message="User registered successfully", data=result)

    @post("/login")
    @inject
    async def login(
        self, service: FromDishka[AuthService], response: Response, data: LoginRequest
    ) -> SuccessResponse:
        result = await service.login(data)

        if isinstance(result, dict) and "refresh" in result:
            refresh_token = result["refresh"]
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                secure=True,
                samesite="strict",
                max_age=7 * 24 * 60 * 60,
            )

        return SuccessResponse(message="Login successful", data=result)

    @post("/logout")
    @inject
    async def logout(self, response: Response) -> SuccessResponse:
        response.delete_cookie(key="refresh_token")
        return SuccessResponse(message="Successfully logged out")

    @post("/refresh")
    @inject
    async def refresh_token(
        self, service: FromDishka[AuthService], request: Request, data: RefreshTokenRequest
    ) -> SuccessResponse:
        result = await service.refresh(data)
        return SuccessResponse(message="Token refreshed successfully", data=result)

    @post("/change-password")
    @inject
    async def change_password(
        self, service: FromDishka[AuthService], request: Request, data: ChangePasswordRequest
    ) -> SuccessResponse:
        await service.change_password(data)
        return SuccessResponse(message="Password changed successfully")

    @get("/me")
    @inject
    async def get_me(
        self,
        service: FromDishka[AuthService],
        request: Request,
    ) -> SuccessResponse:
        result = await service.get_me()
        return SuccessResponse(message="User profile retrieved", data=result)
