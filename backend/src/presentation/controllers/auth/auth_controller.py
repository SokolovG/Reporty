from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, Request, Response, get, post
from litestar.datastructures.cookie import Cookie

from backend.src.application.dto.auth import ChangePasswordData, LoginData, RegisterData
from backend.src.application.use_cases.auth.auth_use_cases import AuthUseCase
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.exceptions.api_exceptions import AuthenticationError
from backend.src.presentation.dto.auth.responses import (
    AccessTokenResponse,
    UserResponse,
)
from backend.src.presentation.dto.auth import ChangePasswordRequest, LoginRequest, RegisterRequest
from backend.src.presentation.dto.auth.responses import TokenInfoResponse
from backend.src.presentation.responses import SuccessResponse
from backend.src.presentation.responses.base_responses import SuccessResponseDTO


class AuthController(Controller):
    @post("/register", return_dto=SuccessResponseDTO)
    @inject
    async def register(
        self,
        request: Request,
        data: RegisterRequest,
        auth_use_case: FromDishka[AuthUseCase],
        converter: FromDishka[Converter],
    ) -> SuccessResponse:
        """Register a new user."""
        register_data = RegisterData(name=data.name, email=data.email, password=data.password)
        domain_user = await auth_use_case.register(register_data)
        user_response = converter.convert(domain_user, UserResponse)
        return SuccessResponse(message="User registered successfully", data=user_response)

    @post("/login")
    @inject
    async def login(
        self,
        request: Request,
        data: LoginRequest,
        auth_use_case: FromDishka[AuthUseCase],
    ) -> Response[SuccessResponse]:
        """Login user and return tokens."""
        login_data = LoginData(email=data.email, password=data.password)
        token_pair = await auth_use_case.login(login_data)

        presentation_token_info = TokenInfoResponse(
            access=token_pair.access_token,
            refresh=token_pair.refresh_token,
            token_type=token_pair.token_type,
        )

        success_response = SuccessResponse(message="Login successful", data=presentation_token_info)
        response = SuccessResponseDTO.create_response_with_cookies(
            request=request,
            success_response=success_response,
            cookies=[
                Cookie(
                    key="refreshToken",
                    value=token_pair.refresh_token,
                    httponly=True,
                    secure=True,
                    samesite="strict",
                    max_age=7 * 24 * 60 * 60,
                ),
                Cookie(
                    key="accessToken",
                    value=token_pair.access_token,
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
    async def logout(self, request: Request) -> Response[SuccessResponse]:
        """Logout user by clearing refresh token cookie."""
        success_response = SuccessResponse(message="Successfully logged out")
        response = SuccessResponseDTO.create_response_with_cookies(
            request=request,
            success_response=success_response,
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
        self,
        request: Request,
        auth_use_case: FromDishka[AuthUseCase],
    ) -> Response[SuccessResponse]:
        """Refresh access token."""
        refresh_token: str | None = request.cookies.get("refreshToken")
        if not refresh_token:
            raise AuthenticationError("No refresh token")

        new_access_token = await auth_use_case.refresh(refresh_token)
        success_response = SuccessResponse(
            message="Token refreshed", data=AccessTokenResponse(access_token=new_access_token)
        )
        response = SuccessResponseDTO.create_response_with_cookies(
            request=request,
            success_response=success_response,
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

    @post("/change-password", return_dto=SuccessResponseDTO)
    @inject
    async def change_password(
        self,
        request: Request,
        data: ChangePasswordRequest,
        auth_use_case: FromDishka[AuthUseCase],
    ) -> SuccessResponse:
        """Change user password."""
        user_id = request.user.id
        change_password_data = ChangePasswordData(
            old_password=data.old_password,
            new_password=data.new_password,
        )
        await auth_use_case.change_password(change_password_data, user_id)
        return SuccessResponse(message="Password changed successfully")

    @get("/me", return_dto=SuccessResponseDTO)
    @inject
    async def get_me(
        self,
        request: Request,
        auth_use_case: FromDishka[AuthUseCase],
        converter: FromDishka[Converter],
    ) -> SuccessResponse:
        """Get current user profile."""
        user_id = request.user.id
        domain_user = await auth_use_case.get_me(user_id)

        user_response = converter.convert(domain_user, UserResponse)
        return SuccessResponse(message="User profile retrieved", data=user_response)
