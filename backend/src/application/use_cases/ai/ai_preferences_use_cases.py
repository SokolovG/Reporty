from backend.src.application.dto.settings import AIPreferencesUpdateData, AIProviderUpdateData
from backend.src.application.use_cases.ai.ai_use_cases import AIUseCases
from backend.src.domain.entities.ai import AIProvider
from backend.src.domain.entities.user import User
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.models import AIProviderKeyModel
from backend.src.infrastructure.database.repositories import (
    AIProviderKeyRepository,
    AIProviderRepository,
    DailyRecordRepository,
    UserRepository,
)
from backend.src.infrastructure.encryption.encryption_service import EncryptionService
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError, NotFoundError


class AIPreferencesUseCases:
    """Use cases for AI preferences management."""

    def __init__(
        self,
        record_repo: DailyRecordRepository,
        user_repository: UserRepository,
        encryption_service: EncryptionService,
        ai_use_cases: AIUseCases,
        ai_provider_repository: AIProviderRepository,
        ai_key_repo: AIProviderKeyRepository,
        converter: Converter,
    ) -> None:
        self.repo = record_repo
        self.user_repository = user_repository
        self.ai_use_cases = ai_use_cases
        self.api_key_repo = ai_key_repo
        self.ai_provider_repository = ai_provider_repository
        self.encryption_service = encryption_service
        self.converter = converter

    async def update_user_preferences(self, user_id: int, data: AIPreferencesUpdateData) -> User:
        """Update user's AI preferences (provider selection, auto-processing).

        Args:
            user_id: ID of the user
            data: AI preferences update data

        Returns:
            Updated AI preferences

        Raises:
            NotFoundError: If user not found
            InternalServerError: If operation fails
        """
        try:
            user = await self.user_repository.get_user_by_id(id=user_id)
            if not user:
                raise NotFoundError("User", user_id)

            user.configure_ai(
                provider_id=data.ai_provider_id,
                auto_process=data.ai_auto_process,
                custom_prompt=data.custom_prompt,
            )

            updated_user = await self.user_repository.update_user(user)

            return updated_user

        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(f"Failed to update AI preferences: {str(e)}")

    async def get_active_providers(self, user_id: int) -> list[AIProvider]:
        """Get only active AI providers with user's API key status.

        Args:
            user_id: ID of the user

        Returns:
            List of active AI providers with models

        Raises:
            InternalServerError: If operation fails
        """
        providers = await self.ai_provider_repository.get_active_providers_with_models()
        return providers

    async def update_provider(
        self, ai_provider_id: int, data: AIProviderUpdateData, user_id: int
    ) -> User:
        """Update an AI provider configuration for user.

        Args:
            ai_provider_id: ID of the AI provider
            data: Provider update data (model selection, API key)
            user_id: ID of the user

        Returns:
            Updated AI provider information

        Raises:
            NotFoundError: If user or provider not found
            InternalServerError: If operation fails
        """
        ai_provider = await self.ai_provider_repository.get_by_id_with_models(ai_provider_id)

        if not ai_provider:
            raise NotFoundError("AIProvider", ai_provider_id)

        user = await self.user_repository.get_user_by_id(id=user_id)
        if not user:
            raise NotFoundError("User", user_id)

        if data.ai_model_id:
            user.ai_model_id = data.ai_model_id

        if data.api_key:
            encrypted_api_key = await self.encryption_service.encrypt(data.api_key)
            api_key = AIProviderKeyModel(
                user_id=user_id,
                ai_provider_id=ai_provider_id,
                encrypted_key=encrypted_api_key,
            )
            await self.api_key_repo.add(api_key)
            await self.api_key_repo.session.commit()

        updated_user = await self.user_repository.update_user(user)
        return updated_user
