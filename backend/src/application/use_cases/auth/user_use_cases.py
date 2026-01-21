from backend.src.domain.entities.user import User
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.repositories import (
    AIModelRepository,
    AIProviderKeyRepository,
    AIProviderRepository,
    ExternalSystemRepository,
    UserRepository,
)
from backend.src.infrastructure.encryption.encryption_service import EncryptionService
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError
from backend.src.presentation.dto import UserUpdateRequest


class UserUseCases:
    """Service for managing user settings and preferences."""

    def __init__(
        self,
        ai_provider_repository: AIProviderRepository,
        ai_models_repository: AIModelRepository,
        user_repository: UserRepository,
        external_system_repository: ExternalSystemRepository,
        encryption_service: EncryptionService,
        api_key_repo: AIProviderKeyRepository,
        converter: Converter,
    ) -> None:
        self.encryption_service = encryption_service
        self.ai_provider_repository = ai_provider_repository
        self.ai_models_repository = ai_models_repository
        self.user_repository = user_repository
        self.external_system_repository = external_system_repository
        self.api_key_repo = api_key_repo
        self.converter = converter

    async def get(self, user_id: int) -> User:
        """Get user with all information."""
        try:
            user = await self.user_repository.get_one(id=user_id)
            return self.converter.convert(user, User)

        except Exception as e:
            raise InternalServerError(f"Failed to get user: {str(e)}", {"user_id": user_id})

    async def update(self, user_id: int, data: UserUpdateRequest) -> User:
        """Update user information."""
        try:
            user = await self.user_repository.update_profile(
                user_id=user_id,
                display_name=data.display_name,
                department=data.department,
                position=data.position,
                email=data.email,
            )
            return self.converter.convert(user, User)

        except Exception as e:
            raise InternalServerError(f"Failed to update user: {str(e)}", {"user_id": user_id})
