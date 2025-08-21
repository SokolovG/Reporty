from adaptix._internal.conversion.facade.func import get_converter

from backend.src.api.dto import (
    RefreshTokenRequest,
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
)
from backend.src.api.dto.auth_dto import UserResponse, TokenInfo
from backend.src.core.exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
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

    async def register(self, data: RegisterRequest) -> UserResponse:
        """Register a new user."""
        user = await self.repo.get_one_or_none(email=data.email)
        if user:
            raise ConflictError(
                "User already exists", {"email": data.email, "reason": "email_taken"}
            )

        hashed_password = self.jwt_service.hash_password(data.password)
        user = await self.repo.create_user(
            email=data.email, name=data.name, password_hash=hashed_password
        )
        await self.notification_service.send_register_notification()
        return self._to_response(user)

    async def login(self, data: LoginRequest) -> TokenInfo:
        """Authenticate user and return tokens."""
        user = await self.repo.get_one_or_none(email=data.email)
        if not user:
            raise AuthenticationError("Invalid email or password", {"email": data.email})

        hashed_password = await self.repo.get_hashed_password(email=data.email)
        success = await self.jwt_service.verify_password(data.password, hashed_password)

        if not success:
            raise AuthenticationError("Invalid email or password", {"email": data.email})

        token_info = await self.jwt_service.login(user_id=user.id)
        return token_info

    async def refresh(self, data: RefreshTokenRequest) -> str:
        """Refresh access token."""
        user = await self.repo.get_one_or_none(email=data.email)
        if not user:
            raise NotFoundError("User", details={"email": data.email})

        # TODO: Проверить refresh токен и создать новый access
        new_access_token = await self.jwt_service.create_access_token(user.id)
        return new_access_token

    async def change_password(self, data: ChangePasswordRequest) -> None:
        """Change user password."""
        user = await self.repo.get_one_or_none()
        if not user:
            raise NotFoundError("User")

        # TODO: Проверить старый пароль и захешировать новый
        new_password_hash = self.jwt_service.hash_password(data.new_password)
        user.password_hash = new_password_hash
        await self.repo.session.commit()

    async def get_me(self) -> UserResponse:
        """Get current user profile."""
        user = await self.repo.get_one_or_none()
        if not user:
            raise NotFoundError("User")

        return self._to_response(user)

    async def forgot_password(self) -> None:
        """Reset user password."""
        # TODO: Implement password reset
        pass
