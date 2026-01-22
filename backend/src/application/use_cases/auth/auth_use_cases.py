from logging import getLogger

from backend.src.application.dto.auth import ChangePasswordData, LoginData, RegisterData
from backend.src.application.ports.notification import NotificationService
from backend.src.domain.entities.user import User
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.repositories import UserRepository
from backend.src.infrastructure.encryption.jwt_service import JWTService
from backend.src.infrastructure.exceptions.api_exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
)
from backend.src.infrastructure.validators.validators import EmailValidator, PasswordValidator
from backend.src.presentation.dto.auth.responses import TokenInfoResponse

logger = getLogger(__name__)


class AuthUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
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
        existing_user = await self.repo.get_one_or_none(email=data.email)
        if existing_user:
            raise ConflictError(
                "User already exists", {"email": data.email, "reason": "email_taken"}
            )

        hashed_password = self.jwt_service.hash_password(data.password)
        user_model = await self.repo.create_user(
            email=data.email,
            name=data.name,
            password_hash=hashed_password,
            is_admin=is_admin,
        )
        domain_user = self.converter.convert(user_model, User)
        await self.notification_service.send_register_notification()
        return domain_user

    async def login(self, data: LoginData) -> TokenInfoResponse:
        """Authenticate user and return tokens."""
        user_model = await self.repo.get_one_or_none(email=data.email)
        if not user_model:
            raise AuthenticationError("Invalid email or password", {"email": data.email})

        domain_user = self.converter.convert(user_model, User)
        if not domain_user.is_active:
            raise AuthenticationError("User account is not active")

        success = await self.jwt_service.verify_password(data.password, user_model.password_hash)
        if not success:
            raise AuthenticationError("Invalid email or password", {"email": data.email})

        return await self.jwt_service.login(user_id=user_model.id)

    async def refresh(self, refresh_token: str) -> str:
        """Refresh access token."""
        payload = await self.jwt_service.verify_token(refresh_token, expected_type="refresh")
        user_id = int(payload["sub"])
        return await self.jwt_service.create_access_token(user_id)

    async def change_password(self, data: ChangePasswordData, user_id: int) -> None:
        """Change user password."""
        user_model = await self.repo.get_one_or_none(id=user_id)
        if not user_model:
            raise NotFoundError("User", user_id)

        success = await self.jwt_service.verify_password(
            data.old_password, user_model.password_hash
        )
        if not success:
            raise AuthenticationError("Current password is incorrect")

        new_password_hash = self.jwt_service.hash_password(data.new_password)
        user_model.password_hash = new_password_hash
        await self.repo.session.commit()

    async def get_me(self, user_id: int) -> User:
        """Get current user profile."""
        user_model = await self.repo.get_one_or_none(id=user_id)
        if not user_model:
            raise NotFoundError("User")

        domain_user = self.converter.convert(user_model, User)

        return domain_user

    async def reset_password(self) -> None:
        """Reset user password."""
        # TODO: Implement password reset
        pass
