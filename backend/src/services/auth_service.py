from adaptix._internal.conversion.facade.func import get_converter

from backend.src.api.dto import (
    RefreshTokenRequest,
    ChangePasswordRequest,
    LogoutRequest,
    LoginRequest,
    RegisterRequest,
)
from backend.src.api.dto.auth_dto import (
    UserResponse,
    SuccessLoginResponse,
    FailedLoginResponse,
    SuccessLogoutResponse,
    FailedRefreshResponse,
    SuccessRefreshResponse,
    SuccessChangePasswordResponse,
    FailedChangePasswordResponse,
)
from backend.src.api.dto.responses import FailResponse
from backend.src.database.models import User
from backend.src.database.repositories import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.repo = user_repository
        self._to_response = get_converter(User, UserResponse)

    async def register(self, data: RegisterRequest) -> UserResponse:
        user = await self.repo.create_user(data)
        return self._to_response(user)

    async def login(self, data: LoginRequest) -> SuccessLoginResponse | FailedLoginResponse:
        user = await self.repo.get_one_or_none(data)  # type: ignore
        if not user:
            return FailedLoginResponse()
        return SuccessLoginResponse()

    async def logout(self, data: LogoutRequest) -> SuccessLogoutResponse:
        user = await self.repo.get(data.username)  # noqa
        # DELETE TOKEN FROM COOKIES
        return SuccessLogoutResponse()

    async def refresh(
        self, data: RefreshTokenRequest
    ) -> SuccessRefreshResponse | FailedRefreshResponse:
        user = await self.repo.get(data.username)
        if not user:
            return FailedRefreshResponse()
        return SuccessRefreshResponse()

    async def change_password(
        self, data: ChangePasswordRequest
    ) -> SuccessChangePasswordResponse | FailedChangePasswordResponse:
        user = await self.repo.get_one_or_none()
        if not user:
            return FailedChangePasswordResponse()
        password_hash = data.new_password
        # HASH PASSWORD
        user.password_hash = password_hash
        await self.repo.session.commit()
        return SuccessChangePasswordResponse()

    async def get_me(self) -> UserResponse | FailResponse:
        user = await self.repo.get_one_or_none()
        if not user:
            return FailResponse()
        return UserResponse()  # type: ignore
