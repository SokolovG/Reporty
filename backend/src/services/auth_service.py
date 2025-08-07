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
    SuccessLogoutResponse,
    FailedRefreshResponse,
    SuccessRefreshResponse,
    SuccessChangePasswordResponse,
    FailedChangePasswordResponse,
)
from backend.src.api.responses import FailResponse
from backend.src.api.responses.base_responses import BaseErrorDetails
from backend.src.core.errors import ErrorCode
from backend.src.database.models import User
from backend.src.database.repositories import UserRepository
from backend.src.services import JWTService, NotificationService


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        jwt_service: JWTService,
        notification_service: NotificationService,
    ) -> None:
        self.repo = user_repository
        self.jwt_service = jwt_service
        self.notification_service = notification_service
        self._to_response = get_converter(User, UserResponse)

    async def register(self, data: RegisterRequest) -> UserResponse | FailResponse:
        user = await self.repo.get_one_or_none(email=data.email)
        if user:
            return FailResponse(
                msg="Authentication failed",
                error_code=ErrorCode.USER_ALREADY_EXISTS,
                details=BaseErrorDetails(
                    reason="User with provided email already exist",
                    context={
                        "email": data.email,
                    },
                ),
            )
        hashed_password = self.jwt_service.hash_password(data.password)
        user = await self.repo.create_user(
            email=data.email, name=data.name, password_hash=hashed_password
        )
        await self.notification_service.send_register_notification()
        return self._to_response(user)

    async def login(self, data: LoginRequest) -> SuccessLoginResponse | FailResponse:
        user = await self.repo.get_one_or_none(data.email)  # type: ignore
        if not user:
            return FailResponse(
                msg="Authentication failed",
                error_code=ErrorCode.USER_NOT_EXIST,
                details=BaseErrorDetails(
                    reason="User with provided email not exist in database",
                    context={
                        "email": data.email,
                    },
                ),
            )
        hashed_password = await self.repo.get_hashed_password(email=data.email)
        success = await self.jwt_service.verify_password(data.password, hashed_password)
        refresh, access = await self.jwt_service.login()
        if success:
            return SuccessLoginResponse(
                refresh=refresh,
                access=access,
            )
        return FailResponse(
            msg="Authentication failed",
            error_code=ErrorCode.INVALID_CREDENTIALS,
            details=BaseErrorDetails(
                reason="Email or password are invalid",
                context={
                    "email": data.email,
                },
            ),
        )

    async def logout(self, data: LogoutRequest) -> SuccessLogoutResponse:
        user = await self.repo.get(data.email)  # noqa
        # DELETE TOKEN FROM COOKIES
        return SuccessLogoutResponse()

    async def refresh(
        self, data: RefreshTokenRequest
    ) -> SuccessRefreshResponse | FailedRefreshResponse:
        user = await self.repo.get(data.email)
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

    async def forgot_password(self) -> None: ...
