from sqlalchemy import select
from adaptix._internal.conversion.facade.func import get_converter

from backend.src.api.dto import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
)
from backend.src.api.dto.auth_dto import UserResponse, TokenInfo
from backend.src.core.exceptions import (
    AuthenticationError,
    ConflictError,
    InternalServerError,
    NotFoundError,
)
from backend.src.database.models import AIProvider, User
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

        result = await self.repo.session.execute(
            select(AIProvider).where(AIProvider.is_active).limit(1)
        )
        default_ai_provider = result.scalar_one_or_none()

        if not default_ai_provider:
            raise InternalServerError("No active AI provider found")

        hashed_password = self.jwt_service.hash_password(data.password)
        user = await self.repo.create_user(
            email=data.email,
            name=data.name,
            password_hash=hashed_password,
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

    async def refresh(self, refresh_token: str) -> str:
        """Refresh access token."""
        payload = await self.jwt_service.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise AuthenticationError("Invalid refresh token")

        user_id = int(payload["sub"])
        return await self.jwt_service.create_access_token(user_id)

    async def change_password(self, data: ChangePasswordRequest, user_id: int) -> None:
        """Change user password."""
        user = await self.repo.get_one_or_none(id=user_id)  # ✅ Добавлен user_id
        if not user:
            raise NotFoundError("User", user_id)

        success = await self.jwt_service.verify_password(data.old_password, user.password_hash)
        if not success:
            raise AuthenticationError("Current password is incorrect")

        new_password_hash = self.jwt_service.hash_password(data.new_password)
        user.password_hash = new_password_hash
        await self.repo.session.commit()

    async def get_me(self, user_id: int) -> UserResponse:
        """Get current user profile."""
        user = await self.repo.get_one_or_none(id=user_id)
        if not user:
            raise NotFoundError("User")

        return self._to_response(user)

    async def forgot_password(self) -> None:
        """Reset user password."""
        # TODO: Implement password reset
        pass
