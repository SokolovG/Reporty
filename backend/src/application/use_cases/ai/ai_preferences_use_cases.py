from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.src.application.use_cases.ai.ai_use_cases import AIUseCases
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.models import AIProviderKeyModel, AIProviderModel
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
    AIPreferencesUpdateRequest,
    AIProviderResponse,
    AIProviderUpdateRequest,
)


class AIPreferencesUseCases:
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
        self, user_id: int, data: AIPreferencesUpdateRequest
    ) -> AIPreferencesResponse:  # TODO: change to domain entity
        """Update user's AI preferences (provider selection, auto-processing)."""
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

        except Exception as e:
            raise InternalServerError(f"Failed to update AI preferences: {str(e)}")

    async def get_active_providers(self, user_id: int) -> list[AIProviderResponse]:
        """Get only active AI providers."""
        try:
            result = await self.ai_provider_repository.session.execute(
                select(AIProviderModel)
                .where(AIProviderModel.is_active)
                .options(selectinload(AIProviderModel.models))
            )
            providers = result.scalars().all()
            response_list = []

            user_provider_ids = await self.api_key_repo.get_all_keys_for_user(user_id=user_id)

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
        self, ai_provider_id: int, data: AIProviderUpdateRequest, user_id: int
    ) -> AIProviderResponse:
        """Update an AI provider."""
        try:
            result = await self.ai_provider_repository.session.execute(
                select(AIProviderModel)
                .options(selectinload(AIProviderModel.models))
                .where(AIProviderModel.id == ai_provider_id)
            )
            ai_provider = result.scalar_one_or_none()
            user = await self.user_repository.get_one_or_none(id=user_id)

            if not user:
                raise NotFoundError("User", user_id)

            if not ai_provider:
                raise NotFoundError("AIProvider", ai_provider_id)

            if data.ai_model_id:
                user.ai_model_id = data.ai_model_id
            if data.api_key:
                encrypted_api_key = await self.encryption_service.encrypt(data.api_key)
                api_key = AIProviderKeyModel(
                    user_id=user_id,
                    ai_provider_id=ai_provider_id,
                    encrypted_key=encrypted_api_key,
                )
                api_key_model = await self.api_key_repo.add(api_key)
                await self.api_key_repo.session.commit()

            await self.ai_provider_repository.session.commit()

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
