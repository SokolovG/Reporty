from backend.src.application.dto.settings import AIPreferencesUpdateData, AIProviderUpdateData
from backend.src.application.use_cases.ai.ai_use_cases import AIUseCases
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
from backend.src.presentation.dto import (
    AIModelResponse,
    AIPreferencesResponse,
    AIProviderResponse,
)


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

    async def update_user_preferences(
        self, user_id: int, data: AIPreferencesUpdateData
    ) -> AIPreferencesResponse:
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
            user = await self.user_repository.get_one_or_none(id=user_id)
            if not user:
                raise NotFoundError("User", user_id)

            if data.ai_provider_id is not None:
                user.ai_provider_id = data.ai_provider_id

            if data.ai_auto_process is not None:
                user.ai_auto_process = data.ai_auto_process

            if data.custom_prompt is not None:
                user.custom_prompt = data.custom_prompt

            await self.user_repository.session.commit()

            return self.converter.convert(user, AIPreferencesResponse)

        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(f"Failed to update AI preferences: {str(e)}")

    async def get_active_providers(self, user_id: int) -> list[AIProviderResponse]:
        """Get only active AI providers with user's API key status.

        Args:
            user_id: ID of the user

        Returns:
            List of active AI providers with models

        Raises:
            InternalServerError: If operation fails
        """
        try:
            providers = await self.ai_provider_repository.get_active_providers_with_models()

            user_provider_ids = await self.api_key_repo.get_all_keys_for_user(user_id=user_id)

            response_list = []
            for provider in providers:
                models_response = [AIModelResponse(id=m.id, name=m.name) for m in provider.models]
                provider_response = AIProviderResponse(
                    id=provider.id,
                    name=provider.name,
                    requires_api_key=provider.requires_api_key,
                    is_active=provider.is_active,
                    models=models_response,
                    is_key_set=provider.id in user_provider_ids,
                )
                response_list.append(provider_response)

            return response_list

        except Exception as e:
            raise InternalServerError(f"Failed to get active AI providers: {str(e)}")

    async def update_provider(
        self, ai_provider_id: int, data: AIProviderUpdateData, user_id: int
    ) -> AIProviderResponse:
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
        try:
            ai_provider = await self.ai_provider_repository.get_by_id_with_models(ai_provider_id)

            if not ai_provider:
                raise NotFoundError("AIProvider", ai_provider_id)

            user = await self.user_repository.get_one_or_none(id=user_id)
            if not user:
                raise NotFoundError("User", user_id)

            if data.ai_model_id:
                user.ai_model_id = data.ai_model_id

            api_key_model = None
            if data.api_key:
                encrypted_api_key = await self.encryption_service.encrypt(data.api_key)
                api_key = AIProviderKeyModel(
                    user_id=user_id,
                    ai_provider_id=ai_provider_id,
                    encrypted_key=encrypted_api_key,
                )
                api_key_model = await self.api_key_repo.add(api_key)
                await self.api_key_repo.session.commit()

            await self.user_repository.session.commit()

            models_response = [AIModelResponse(id=m.id, name=m.name) for m in ai_provider.models]
            return AIProviderResponse(
                id=ai_provider.id,
                name=ai_provider.name,
                requires_api_key=ai_provider.requires_api_key,
                is_active=ai_provider.is_active,
                models=models_response,
                is_key_set=True if api_key_model else False,
            )

        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(
                f"Failed to update AI provider: {str(e)}", {"ai_provider_id": ai_provider_id}
            )
