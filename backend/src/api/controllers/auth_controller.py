from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get, post, Request, Response

from backend.src.api.dto import (
    ChangePasswordRequest,
    RefreshTokenRequest,
    LoginRequest,
    RegisterRequest,
    SuccessResponseDTO,
)
from backend.src.api.responses.base_responses import SuccessResponse
from backend.src.services import AuthService


class AuthController(Controller):
    @post("/register", return_dto=SuccessResponseDTO)
    @inject
    async def register(
        self, service: FromDishka[AuthService], request: Request, data: RegisterRequest
    ) -> SuccessResponse:
        """Register a new user."""
        user = await service.register(data)
        return SuccessResponse(message="User registered successfully", data=user)

    @post("/login")
    @inject
    async def login(
        self, service: FromDishka[AuthService], response: Response, data: LoginRequest
    ) -> SuccessResponse:
        """Login user and return tokens."""
        token_info = await service.login(data)

        # Set refresh token in httpOnly cookie
        response.set_cookie(
            "refresh_token",
            token_info.refresh,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=7 * 24 * 60 * 60,  # 7 days
        )

        return SuccessResponse(message="Login successful", data=token_info)

    @post("/logout")
    @inject
    async def logout(self, response: Response) -> SuccessResponse:
        """Logout user by clearing refresh token cookie."""
        response.delete_cookie(key="refresh_token")
        return SuccessResponse(message="Successfully logged out")

    @post("/refresh")
    @inject
    async def refresh_token(
        self, service: FromDishka[AuthService], request: Request, data: RefreshTokenRequest
    ) -> SuccessResponse:
        """Refresh access token."""
        new_token = await service.refresh(data)
        return SuccessResponse(
            message="Token refreshed successfully", data={"access_token": new_token}
        )

    @post("/change-password")
    @inject
    async def change_password(
        self, service: FromDishka[AuthService], request: Request, data: ChangePasswordRequest
    ) -> SuccessResponse:
        """Change user password."""
        user_id = request.user.id
        await service.change_password(data, user_id)
        return SuccessResponse(message="Password changed successfully")

    @get("/me")
    @inject
    async def get_me(
        self,
        service: FromDishka[AuthService],
        request: Request,
    ) -> SuccessResponse:
        """Get current user profile."""
        user_id = request.user.id
        user = await service.get_me(user_id)
        return SuccessResponse(message="User profile retrieved", data=user)
