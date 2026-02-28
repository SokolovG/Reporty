from logging import getLogger

from backend.src.application.dto.auth import ChangePasswordData, LoginData, RegisterData
from backend.src.application.ports.notification import NotificationService
from backend.src.application.ports.repositories import IUserRepository
from backend.src.domain.entities.user import User
from backend.src.domain.value_objects import TokenPair
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.encryption.jwt_service import JWTService
from backend.src.infrastructure.exceptions.api_exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
)
from backend.src.infrastructure.validators.validators import EmailValidator, PasswordValidator

logger = getLogger(__name__)


class AuthUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        jwt_service: JWTService,
        notification_service: NotificationService,
        converter: Converter,
    ) -> None:
        self.repo = user_repository
        self.jwt_service = jwt_service
        self.notification_service = notification_service
        self.converter = converter

    async def register(self, data: RegisterData, is_admin: bool = False) -> User:
        """Register a new user."""
        EmailValidator.validate(data.email)
        PasswordValidator.validate(data.password)
        existing_user = await self.repo.get_user_by_email(email=data.email)
        if existing_user:
            raise ConflictError(
                "User already exists", {"email": data.email, "reason": "email_taken"}
            )

        hashed_password = self.jwt_service.hash_password(data.password)
        user = await self.repo.create_user(data, hashed_password)
        await self.notification_service.send_register_notification()
        return user

    async def login(self, data: LoginData) -> TokenPair:
        """Authenticate user and return tokens."""
        user = await self.repo.get_user_by_email(email=data.email)
        if not user:
            raise AuthenticationError("Invalid email or password", {"email": data.email})
        if not user.is_active:
            raise AuthenticationError("User account is not active")

        success = await self.jwt_service.verify_password(data.password, user.password_hash)
        if not success:
            raise AuthenticationError("Invalid email or password", {"email": data.email})

        token = await self.jwt_service.login(user_id=user.id)
        return token

    async def refresh(self, refresh_token: str) -> str:
        """Refresh access token."""
        payload = await self.jwt_service.verify_token(refresh_token, expected_type="refresh")
        user_id = int(payload["sub"])
        token = await self.jwt_service.create_access_token(user_id)
        return token

    async def logout(self, access_token: str | None, refresh_token: str | None) -> None:
        """Invalidate tokens on logout."""
        if access_token:
            await self.jwt_service.blacklist_token(access_token)
        if refresh_token:
            await self.jwt_service.blacklist_token(refresh_token)

    async def change_password(self, data: ChangePasswordData, user_id: int) -> None:
        """Change user password."""
        user = await self.repo.get_user_by_id(id=user_id)
        if not user:
            raise NotFoundError("User", user_id)

        success = await self.jwt_service.verify_password(data.old_password, user.password_hash)
        if not success:
            raise AuthenticationError("Current password is incorrect")

        new_password_hash = self.jwt_service.hash_password(data.new_password)
        user.password_hash = new_password_hash
        await self.repo.update_user(user)

    async def get_me(self, user_id: int) -> User:
        """Get current user profile."""
        user = await self.repo.get_user_by_id(id=user_id)
        if not user:
            raise NotFoundError("User")

        return user

    async def reset_password(self) -> None:
        """Reset user password."""
        # TODO: Implement password reset
        pass
