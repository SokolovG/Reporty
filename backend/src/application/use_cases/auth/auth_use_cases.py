from logging import getLogger

from backend.src.infrastructure.database.repositories import UserRepository
from backend.src.infrastructure.encryption.jwt_service import JWTService
from backend.src.infrastructure.exceptions.api_exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
)
from backend.src.infrastructure.validators.validators import EmailValidator, PasswordValidator
from backend.src.presentation.dto import (
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    TokenInfo,
    UserResponse,
)

logger = getLogger(__name__)


class AuthUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        jwt_service: JWTService,
        notification_service: NotificationService,
    ) -> None:
        self.repo = user_repository
        self.jwt_service = jwt_service
        self.notification_service = notification_service

    async def register(self, data: RegisterRequest, is_admin: bool = False) -> UserResponse:
        """Register a new user."""
        EmailValidator.validate(data.email)
        PasswordValidator.validate(data.password)
        user = await self.repo.get_one_or_none(email=data.email)
        if user:
            raise ConflictError(
                "User already exists", {"email": data.email, "reason": "email_taken"}
            )

        hashed_password = self.jwt_service.hash_password(data.password)
        user = await self.repo.create_user(
            email=data.email, name=data.name, password_hash=hashed_password, is_admin=is_admin
        )
        await self.notification_service.send_register_notification()
        return user_to_response(user)

    async def login(self, data: LoginRequest) -> TokenInfo:
        """Authenticate user and return tokens."""
        user = await self.repo.get_one_or_none(email=data.email)
        if not user:
            raise AuthenticationError("Invalid email or password", {"email": data.email})

        success = await self.jwt_service.verify_password(data.password, user.password_hash)

        if not success:
            raise AuthenticationError("Invalid email or password", {"email": data.email})

        token_info = await self.jwt_service.login(user_id=user.id)
        return token_info

    async def refresh(self, refresh_token: str) -> str:
        """Refresh access token."""
        payload = await self.jwt_service.verify_token(refresh_token, expected_type="refresh")
        user_id = int(payload["sub"])
        return await self.jwt_service.create_access_token(user_id)

    async def change_password(self, data: ChangePasswordRequest, user_id: int) -> None:
        """Change user password."""
        user = await self.repo.get_one_or_none(id=user_id)
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

        return user_to_response(user)

    async def reset_password(self) -> None:
        """Reset user password."""
        # TODO: Implement password reset
        pass
