from adaptix.conversion import get_converter
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.src.api.dto.settings_dto import (
    AIModelResponse,
    AIPreferencesUpdateRequest,
    AIPreferencesResponse,
)
from backend.src.core.exceptions import NotFoundError, InternalServerError
from backend.src.database.repositories import (
    AIProviderRepository,
    UserRepository,
    ExternalSystemRepository,
    AIModelRepository,
)
from backend.src.database.models import TaskType, AIProvider, User, ExternalSystem
from backend.src.api.dto import (
    TaskTypeRequest,
    TaskTypeUpdateRequest,
    TaskTypeResponse,
    AIProviderResponse,
    ExternalSystemResponse,
    AIProviderUpdateRequest,
    ExternalSystemUpdateRequest,
)
from backend.src.api.dto.auth_dto import UserResponse, UserUpdateRequest
from backend.src.services.crypto_service import CryptoService


class SettingsService:
    def __init__(
        self,
        ai_provider_repository: AIProviderRepository,
        ai_models_repository: AIModelRepository,
        user_repository: UserRepository,
        external_system_repository: ExternalSystemRepository,
        crypto_service: CryptoService,
    ) -> None:
        self.crypto_service = crypto_service
        self.ai_provider_repository = ai_provider_repository
        self.ai_models_repository = ai_models_repository
        self.user_repository = user_repository
        self.external_system_repository = external_system_repository
        self._to_task_type_response = get_converter(TaskType, TaskTypeResponse)
        self._to_ai_provider_response = get_converter(AIProvider, AIProviderResponse)
        self._to_external_system_response = get_converter(ExternalSystem, ExternalSystemResponse)
        self._to_user_response = get_converter(User, UserResponse)
        self._to_ai_preferences_response = get_converter(User, AIPreferencesResponse)

    async def get_task_types(self, user_id: int) -> list[TaskTypeResponse]:
        """Get all task types for a user."""
        try:
            result = await self.user_repository.session.execute(
                select(User).options(selectinload(User.task_types)).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                return []

            return [self._to_task_type_response(task_type) for task_type in user.task_types]
        except Exception as e:
            raise InternalServerError(f"Failed to get task types: {str(e)}", {"user_id": user_id})

    async def create_task_type(self, user_id: int, data: TaskTypeRequest) -> TaskTypeResponse:
        """Create a new task type for a user."""
        try:
            result = await self.user_repository.session.execute(
                select(User).options(selectinload(User.task_types)).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                raise NotFoundError("User", details={"user_id": user_id})

            task_type = TaskType(
                user_id=user.id,
                title=data.title,
                color=data.color,
            )
            user.task_types.append(task_type)
            await self.user_repository.session.commit()
            return self._to_task_type_response(task_type)
        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(f"Failed to create task type: {str(e)}", {"user_id": user_id})

    async def update_task_type(
        self, task_type_id: int, data: TaskTypeUpdateRequest, user_id: int
    ) -> TaskTypeResponse:
        """Update an existing task type."""
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

            if data.title is not None:
                task_type.title = data.title
            if data.color is not None:
                task_type.color = data.color
            if data.is_active is not None:
                task_type.is_active = data.is_active

            await self.user_repository.session.commit()
            return self._to_task_type_response(task_type)
        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(
                f"Failed to update task type: {str(e)}", {"task_type_id": task_type_id}
            )

    async def delete_task_type(self, task_type_id: int, user_id: int) -> None:
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
            return self._to_ai_preferences_response(user)

        except Exception as e:
            raise InternalServerError(f"Failed to update AI preferences: {str(e)}")

    async def get_active_ai_providers(self) -> list[AIProviderResponse]:
        """Get only active AI providers."""
        try:
            result = await self.ai_provider_repository.session.execute(
                select(AIProvider)
                .where(AIProvider.is_active)
                .options(selectinload(AIProvider.models))
            )
            providers = result.scalars().all()
            response_list = []
            for provider in providers:
                models_response = [AIModelResponse(id=m.id, name=m.name) for m in provider.models]
                provider_response = AIProviderResponse(
                    id=provider.id,
                    name=provider.name,
                    requires_api_key=provider.requires_api_key,
                    is_active=provider.is_active,
                    models=models_response,
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
            if data.api_key is not None and data.api_key.strip():
                encrypted_api_key = self.crypto_service.encrypt(data.api_key)  # noqa

            await self.ai_provider_repository.session.commit()

            models_response = [AIModelResponse(id=m.id, name=m.name) for m in ai_provider.models]
            return AIProviderResponse(
                id=ai_provider.id,
                name=ai_provider.name,
                requires_api_key=ai_provider.requires_api_key,
                is_active=ai_provider.is_active,
                models=models_response,
            )

        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(
                f"Failed to update AI provider: {str(e)}", {"ai_provider_id": ai_provider_id}
            )

    async def get_user(self, user_id: int) -> UserResponse:
        """Get user with all information."""
        try:
            user = await self.user_repository.get_one(id=user_id)
            return self._to_user_response(user)
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
            return self._to_user_response(user)
        except Exception as e:
            raise InternalServerError(f"Failed to update user: {str(e)}", {"user_id": user_id})

    async def get_external_systems(self) -> list[ExternalSystemResponse]:
        """Get all external systems."""
        try:
            result = await self.external_system_repository.session.execute(select(ExternalSystem))
            return [self._to_external_system_response(s) for s in result.scalars().all()]
        except Exception as e:
            raise InternalServerError(f"Failed to get external systems: {str(e)}")

    async def get_active_external_systems(self) -> list[ExternalSystemResponse]:
        """Get only active external systems."""
        try:
            result = await self.external_system_repository.session.execute(
                select(ExternalSystem).where(ExternalSystem.is_active == True)  # noqa: E712
            )
            return [self._to_external_system_response(s) for s in result.scalars().all()]
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
            return self._to_external_system_response(updated_system)
        except Exception as e:
            raise InternalServerError(
                f"Failed to update external system: {str(e)}", {"system_id": system_id}
            )
