"""
Settings Service - handles user preferences and configuration.

TODO: Split into domain-specific services:
- AIPreferencesService (ai domain)
- TaskTypeService (records domain)
- UserProfileService (auth domain)
- ExternalSystemService (shared domain)
"""

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.src.api.dto import (
    AIProviderResponse,
    AIProviderUpdateRequest,
    ExternalSystemResponse,
    ExternalSystemUpdateRequest,
)
from backend.src.api.dto.auth.requests import UserUpdateRequest
from backend.src.api.dto.auth.responses import UserResponse
from backend.src.api.dto.converters import (
    external_system_to_response,
    to_ai_preferences_response,
    user_to_response,
)
from backend.src.api.dto.settings.requests import AIPreferencesUpdateRequest
from backend.src.api.dto.settings.responses import AIModelResponse, AIPreferencesResponse
from backend.src.core.exceptions import InternalServerError, NotFoundError
from backend.src.database.models import AIProvider, AIProviderKey, ExternalSystem, TaskType, User
from backend.src.database.repositories import (
    AIModelRepository,
    AIProviderRepository,
    ExternalSystemRepository,
    UserRepository,
)
from backend.src.database.repositories.ai.ai_repository import AIProviderKeyRepository
from backend.src.services.shared.encryption_service import EncryptionService


class SettingsService:
    """Service for managing user settings and preferences."""

    def __init__(
        self,
        ai_provider_repository: AIProviderRepository,
        ai_models_repository: AIModelRepository,
        user_repository: UserRepository,
        external_system_repository: ExternalSystemRepository,
        encryption_service: EncryptionService,
        api_key_repo: AIProviderKeyRepository,
    ) -> None:
        self.encryption_service = encryption_service
        self.ai_provider_repository = ai_provider_repository
        self.ai_models_repository = ai_models_repository
        self.user_repository = user_repository
        self.external_system_repository = external_system_repository
        self.api_key_repo = api_key_repo

        """Delete a task type."""
        try:
            result = await self.user_repository.session.execute(
                select(User)
                .options(selectinload(User.task_types))
                .join(TaskType, User.id == TaskType.user_id)
                .where(TaskType.id == task_type_id)
                .where(User.id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                raise NotFoundError("TaskType", task_type_id)

            task_type = next((tt for tt in user.task_types if tt.id == task_type_id), None)
            if not task_type:
                raise NotFoundError("TaskType", task_type_id)

            user.task_types.remove(task_type)
            await self.user_repository.session.commit()
        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(
                f"Failed to delete task type: {str(e)}", {"task_type_id": task_type_id}
            )

    # AI Preferences Management
    async def update_user_ai_preferences(
        self, user_id: int, data: AIPreferencesUpdateRequest
    ) -> AIPreferencesResponse:
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
            return to_ai_preferences_response(user)

        except Exception as e:
            raise InternalServerError(f"Failed to update AI preferences: {str(e)}")

    async def get_active_ai_providers(self, user_id: int) -> list[AIProviderResponse]:
        """Get only active AI providers."""
        try:
            result = await self.ai_provider_repository.session.execute(
                select(AIProvider)
                .where(AIProvider.is_active)
                .options(selectinload(AIProvider.models))
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

    async def update_ai_provider(
        self, ai_provider_id: int, data: AIProviderUpdateRequest, user_id: int
    ) -> AIProviderResponse:
        """Update an AI provider."""
        try:
            result = await self.ai_provider_repository.session.execute(
                select(AIProvider)
                .options(selectinload(AIProvider.models))
                .where(AIProvider.id == ai_provider_id)
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
                api_key = AIProviderKey(
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

    # User Management
    async def get_user(self, user_id: int) -> UserResponse:
        """Get user with all information."""
        try:
            user = await self.user_repository.get_one(id=user_id)
            return user_to_response(user)
        except Exception as e:
            raise InternalServerError(f"Failed to get user: {str(e)}", {"user_id": user_id})

    async def update_user(self, user_id: int, data: UserUpdateRequest) -> UserResponse:
        """Update user information."""
        try:
            user = await self.user_repository.update_profile(
                user_id=user_id,
                display_name=data.display_name,
                department=data.department,
                position=data.position,
                email=data.email,
            )
            return user_to_response(user)
        except Exception as e:
            raise InternalServerError(f"Failed to update user: {str(e)}", {"user_id": user_id})

    # External Systems Management
    async def get_external_systems(self) -> list[ExternalSystemResponse]:
        """Get all external systems."""
        try:
            result = await self.external_system_repository.session.execute(select(ExternalSystem))
            return [external_system_to_response(s) for s in result.scalars().all()]
        except Exception as e:
            raise InternalServerError(f"Failed to get external systems: {str(e)}")

    async def get_active_external_systems(self) -> list[ExternalSystemResponse]:
        """Get only active external systems."""
        try:
            result = await self.external_system_repository.session.execute(
                select(ExternalSystem).where(ExternalSystem.is_active == True)  # noqa: E712
            )
            return [external_system_to_response(s) for s in result.scalars().all()]
        except Exception as e:
            raise InternalServerError(f"Failed to get active external systems: {str(e)}")

    async def update_external_system(
        self, system_id: int, data: ExternalSystemUpdateRequest
    ) -> ExternalSystemResponse:
        """Update an external system."""
        try:
            system = await self.external_system_repository.get(system_id)

            if data.name is not None:
                system.name = data.name
            if data.display_name is not None:
                system.display_name = data.display_name
            if data.api_config is not None:
                system.api_config = data.api_config
            if data.is_active is not None:
                system.is_active = data.is_active

            updated_system = await self.external_system_repository.update(system)
            await self.external_system_repository.session.commit()
            return external_system_to_response(updated_system)
        except Exception as e:
            raise InternalServerError(
                f"Failed to update external system: {str(e)}", {"system_id": system_id}
            )
