from adaptix._internal.conversion.facade.func import get_converter

from backend.src.api.dto import (
    RefreshTokenRequest,
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
)
from backend.src.api.dto.auth_dto import UserResponse
from backend.src.api.responses import ErrorResponse, SuccessResponse
from backend.src.api.utils.error_utils import (
    user_already_exists_error,
    user_not_found_error,
    auth_error,
)
from backend.src.api.utils.success_utils import (
    login_success,
    user_registration_success,
    refresh_success,
    password_change_success,
    user_profile_success,
)
from backend.src.database.models import User
from backend.src.database.repositories import UserRepository
from backend.src.services.jwt_service import JWTService
from backend.src.services.notification_service import NotificationService


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

    async def register(self, data: RegisterRequest) -> SuccessResponse | ErrorResponse:
        user = await self.repo.get_one_or_none(email=data.email)
        if user:
            return user_already_exists_error(data.email)

        hashed_password = self.jwt_service.hash_password(data.password)
        user = await self.repo.create_user(
            email=data.email, name=data.name, password_hash=hashed_password
        )
        await self.notification_service.send_register_notification()
        user_response = self._to_response(user)
        return user_registration_success(user_response)

    async def login(self, data: LoginRequest) -> SuccessResponse | ErrorResponse:
        user = await self.repo.get_one_or_none(email=data.email)
        if not user:
            return user_not_found_error(data.email)

        hashed_password = await self.repo.get_hashed_password(email=data.email)
        success = await self.jwt_service.verify_password(data.password, hashed_password)

        if not success:
            return auth_error("Invalid email or password", {"email": data.email})

        token_info = await self.jwt_service.login(user_id=user.id)
        return login_success(token_info)

    async def refresh(self, data: RefreshTokenRequest) -> SuccessResponse | ErrorResponse:
        user = await self.repo.get_one_or_none(email=data.email)
        if not user:
            return user_not_found_error(data.email)

        # TODO: Проверить refresh токен и создать новый access
        new_access_token = await self.jwt_service.create_access_token(user.id)
        return refresh_success(new_access_token)

    async def change_password(self, data: ChangePasswordRequest) -> SuccessResponse | ErrorResponse:
        user = await self.repo.get_one_or_none()
        if not user:
            return auth_error("User not found")

        # TODO: Проверить старый пароль и захешировать новый
        new_password_hash = self.jwt_service.hash_password(data.new_password)
        user.password_hash = new_password_hash
        await self.repo.session.commit()
        return password_change_success()

    async def get_me(self) -> SuccessResponse | ErrorResponse:
        user = await self.repo.get_one_or_none()
        if not user:
            return auth_error("User not found")

        user_response = self._to_response(user)
        return user_profile_success(user_response)

    async def forgot_password(self) -> None: ...
