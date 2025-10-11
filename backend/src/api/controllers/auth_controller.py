from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get, post, Request, Response
from litestar.datastructures.cookie import Cookie

from backend.src.api.dto import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    SuccessResponseDTO,
)
from backend.src.api.dto.auth_dto import AccessTokenResponse
from backend.src.api.responses.base_responses import SuccessResponse
from backend.src.core.exceptions import AuthenticationError
from backend.src.services import AuthService


class AuthController(Controller):
    @post("/register", return_dto=SuccessResponseDTO)
    @inject
    async def register(
        self, service: FromDishka[AuthService], data: RegisterRequest
    ) -> SuccessResponse:
        """Register a new user."""
        user = await service.register(data)
        return SuccessResponse(message="User registered successfully", data=user)

    @post("/login")
    @inject
    async def login(
        self, service: FromDishka[AuthService], data: LoginRequest
    ) -> Response[SuccessResponse]:
        """Login user and return tokens."""
        token_info = await service.login(data)

        success_response = SuccessResponse(message="Login successful", data=token_info)

        response = Response(
            content=success_response,
            status_code=200,
            cookies=[
                Cookie(
                    key="refreshToken",
                    value=token_info.refresh,
                    httponly=True,
                    secure=True,
                    samesite="strict",
                    max_age=7 * 24 * 60 * 60,
                ),
                Cookie(
                    key="accessToken",
                    value=token_info.access,
                    httponly=True,
                    secure=True,
                    samesite="strict",
                    max_age=15 * 60,
                ),
            ],
        )
        return response

    @post("/logout")
    @inject
    async def logout(self) -> Response[SuccessResponse]:
        """Logout user by clearing refresh token cookie."""
        success_response = SuccessResponse(message="Successfully logged out")

        response = Response(
            content=success_response,
            status_code=200,
            cookies=[
                Cookie(
                    key="refreshToken",
                    value="",
                    httponly=True,
                    secure=True,
                    samesite="strict",
                    max_age=0,
                ),
                Cookie(
                    key="accessToken",
                    value="",
                    httponly=True,
                    secure=True,
                    samesite="strict",
                    max_age=0,
                ),
            ],
        )
        return response

    @post("/refresh")
    @inject
    async def refresh_token(
        self, service: FromDishka[AuthService], request: Request
    ) -> Response[SuccessResponse]:
        """Refresh access token."""
        refresh_token: str | None = request.cookies.get("refreshToken")
        if not refresh_token:
            raise AuthenticationError("No refresh token")

        new_access_token = await service.refresh(refresh_token)
        response = Response(
            content=SuccessResponse(
                message="Token refreshed", data=AccessTokenResponse(access_token=new_access_token)
            ),
            status_code=200,
            cookies=[
                Cookie(
                    key="accessToken",
                    value=new_access_token,
                    httponly=True,
                    secure=True,
                    samesite="strict",
                    max_age=15 * 60,
                )
            ],
        )
        return response

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
