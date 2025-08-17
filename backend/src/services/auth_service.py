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
    SuccessRefreshResponse,
    SuccessChangePasswordResponse,
)
from backend.src.api.responses import ErrorResponse
from backend.src.api.utils.error_utils import (
    user_already_exists_error,
    user_not_found_error,
    auth_error,
)
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

    async def register(self, data: RegisterRequest) -> UserResponse | ErrorResponse:
        user = await self.repo.get_one_or_none(email=data.email)
        if user:
            return user_already_exists_error(data.email)

        hashed_password = self.jwt_service.hash_password(data.password)
        user = await self.repo.create_user(
            email=data.email, name=data.name, password_hash=hashed_password
        )
        await self.notification_service.send_register_notification()
        return self._to_response(user)

    async def login(self, data: LoginRequest) -> SuccessLoginResponse | ErrorResponse:
        user = await self.repo.get_one_or_none(data.email)  # type: ignore
        if not user:
            return user_not_found_error(data.email)

        hashed_password = await self.repo.get_hashed_password(email=data.email)
        success = await self.jwt_service.verify_password(data.password, hashed_password)
        token_info = await self.jwt_service.login(user_id=user.id)

        if success:
            return SuccessLoginResponse(
                access=token_info.access,
            )

        return auth_error("Invalid email or password", {"email": data.email})

    async def logout(self, data: LogoutRequest) -> SuccessLogoutResponse | ErrorResponse:
        user = await self.repo.get(data.email)  # noqa
        # DELETE TOKEN FROM COOKIES
        return SuccessLogoutResponse()

    async def refresh(self, data: RefreshTokenRequest) -> SuccessRefreshResponse | ErrorResponse:
        user = await self.repo.get(data.email)
        if not user:
            return user_not_found_error(data.email)
        return SuccessRefreshResponse()

    async def change_password(
        self, data: ChangePasswordRequest
    ) -> SuccessChangePasswordResponse | ErrorResponse:
        user = await self.repo.get_one_or_none()
        if not user:
            return auth_error("User not found")
        password_hash = data.new_password
        # HASH PASSWORD
        user.password_hash = password_hash
        await self.repo.session.commit()
        return SuccessChangePasswordResponse()

    async def get_me(self) -> UserResponse | ErrorResponse:
        user = await self.repo.get_one_or_none()
        if not user:
            return auth_error("User not found")
        return UserResponse()  # type: ignore

    async def forgot_password(self) -> None: ...
