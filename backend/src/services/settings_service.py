from adaptix.conversion import get_converter
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.src.database.repositories import (
    AIProviderRepository,
    UserProfileRepository,
    ExternalSystemRepository,
)
from backend.src.database.models import TaskType, AIProvider, UserProfile, ExternalSystem
from backend.src.api.dto import (
    TaskTypeRequest,
    TaskTypeUpdateRequest,
    TaskTypeResponse,
    AIProviderResponse,
    UserProfileResponse,
    ExternalSystemResponse,
    UserProfileUpdateRequest,
    AIProviderUpdateRequest,
    ExternalSystemUpdateRequest,
)


class SettingsService:
    def __init__(
        self,
        ai_provider_repository: AIProviderRepository,
        user_profile_repository: UserProfileRepository,
        external_system_repository: ExternalSystemRepository,
    ) -> None:
        self.ai_provider_repository = ai_provider_repository
        self.user_profile_repository = user_profile_repository
        self.external_system_repository = external_system_repository
        self._to_task_type_response = get_converter(TaskType, TaskTypeResponse)
        self._to_ai_provider_response = get_converter(AIProvider, AIProviderResponse)
        self._to_user_profile_response = get_converter(UserProfile, UserProfileResponse)
        self._to_external_system_response = get_converter(ExternalSystem, ExternalSystemResponse)

    # TaskType methods
    async def get_task_types(self, user_id: int) -> list[TaskTypeResponse]:
        """Get all task types for a user."""
        result = await self.user_profile_repository.session.execute(
            select(UserProfile)
            .options(selectinload(UserProfile.task_types))
            .where(UserProfile.user_id == user_id)
        )
        user_profile = result.scalar_one_or_none()

        if not user_profile:
            return []

        return [self._to_task_type_response(task_type) for task_type in user_profile.task_types]

    async def create_task_type(self, user_id: int, data: TaskTypeRequest) -> TaskTypeResponse:
        """Create a new task type for a user."""
        result = await self.user_profile_repository.session.execute(
            select(UserProfile)
            .options(selectinload(UserProfile.task_types))
            .where(UserProfile.user_id == user_id)
        )
        user_profile = result.scalar_one_or_none()

        if not user_profile:
            raise ValueError(f"UserProfile for user_id {user_id} not found")

        task_type = TaskType(
            user_profile_id=user_profile.id,
            title=data.title,
            color=data.color,
        )
        user_profile.task_types.append(task_type)
        await self.user_profile_repository.session.commit()
        return self._to_task_type_response(task_type)

    async def update_task_type(
        self, task_type_id: int, data: TaskTypeUpdateRequest
    ) -> TaskTypeResponse:
        """Update an existing task type."""

        result = await self.user_profile_repository.session.execute(
            select(UserProfile)
            .options(selectinload(UserProfile.task_types))
            .join(TaskType, UserProfile.id == TaskType.user_profile_id)
            .where(TaskType.id == task_type_id)
        )
        user_profile = result.scalar_one_or_none()

        if not user_profile:
            raise ValueError(f"TaskType with id {task_type_id} not found")

        task_type = next((tt for tt in user_profile.task_types if tt.id == task_type_id), None)
        if not task_type:
            raise ValueError(f"TaskType with id {task_type_id} not found")

        if data.title is not None:
            task_type.title = data.title
        if data.color is not None:
            task_type.color = data.color
        if data.is_active is not None:
            task_type.is_active = data.is_active

        await self.user_profile_repository.session.commit()
        return self._to_task_type_response(task_type)

    async def delete_task_type(self, task_type_id: int) -> None:
        """Delete a task type."""

        result = await self.user_profile_repository.session.execute(
            select(UserProfile)
            .options(selectinload(UserProfile.task_types))
            .join(TaskType, UserProfile.id == TaskType.user_profile_id)
            .where(TaskType.id == task_type_id)
        )
        user_profile = result.scalar_one_or_none()

        if not user_profile:
            raise ValueError(f"TaskType with id {task_type_id} not found")

        task_type = next((tt for tt in user_profile.task_types if tt.id == task_type_id), None)
        if not task_type:
            raise ValueError(f"TaskType with id {task_type_id} not found")

        user_profile.task_types.remove(task_type)
        await self.user_profile_repository.session.commit()

    # AIProvider methods
    async def get_ai_providers(self) -> list[AIProviderResponse]:
        """Get all AI providers."""

        result = await self.ai_provider_repository.session.execute(select(AIProvider))
        return [self._to_ai_provider_response(p) for p in result.scalars().all()]

    async def get_active_ai_providers(self) -> list[AIProviderResponse]:
        """Get only active AI providers."""
        from sqlalchemy import select

        result = await self.ai_provider_repository.session.execute(
            select(AIProvider).where(AIProvider.is_active == True)  # noqa: E712
        )
        return [self._to_ai_provider_response(p) for p in result.scalars().all()]

    async def update_ai_provider(
        self, ai_provider_id: int, data: AIProviderUpdateRequest
    ) -> AIProviderResponse:
        """Update an AI provider."""
        ai_provider = await self.ai_provider_repository.get(ai_provider_id)
        if data.name is not None:
            ai_provider.name = data.name
        if data.base_prompt is not None:
            ai_provider.base_prompt = data.base_prompt
        if data.model_name is not None:
            ai_provider.model_name = data.model_name
        if data.requires_api_key is not None:
            ai_provider.requires_api_key = data.requires_api_key
        if data.is_active is not None:
            ai_provider.is_active = data.is_active
        updated_ai_provider = await self.ai_provider_repository.update(ai_provider)
        await self.ai_provider_repository.session.commit()
        return self._to_ai_provider_response(updated_ai_provider)

    # UserProfile methods
    async def get_user_profile(self, user_id: int) -> UserProfileResponse:
        """Get user profile with settings."""
        result = await self.user_profile_repository.session.execute(
            select(UserProfile)
            .options(selectinload(UserProfile.task_types))
            .where(UserProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()

        if not profile:
            raise ValueError(f"UserProfile for user_id {user_id} not found")

        return self._to_user_profile_response(profile)

    async def update_user_profile(
        self, user_id: int, data: UserProfileUpdateRequest
    ) -> UserProfileResponse:
        """Update user profile settings."""
        result = await self.user_profile_repository.session.execute(
            select(UserProfile)
            .options(selectinload(UserProfile.task_types))
            .where(UserProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()

        if not profile:
            raise ValueError(f"UserProfile for user_id {user_id} not found")

        if data.display_name is not None:
            profile.display_name = data.display_name
        if data.department is not None:
            profile.department = data.department
        if data.position is not None:
            profile.position = data.position
        if data.ai_auto_process is not None:
            profile.ai_auto_process = data.ai_auto_process
        if data.ai_provider_id is not None:
            profile.ai_provider_id = data.ai_provider_id
        updated_profile = await self.user_profile_repository.update(profile)
        await self.user_profile_repository.session.commit()
        return self._to_user_profile_response(updated_profile)

    # ExternalSystem methods
    async def get_external_systems(self) -> list[ExternalSystemResponse]:
        """Get all external systems."""

        result = await self.external_system_repository.session.execute(select(ExternalSystem))
        return [self._to_external_system_response(s) for s in result.scalars().all()]

    async def get_active_external_systems(self) -> list[ExternalSystemResponse]:
        """Get only active external systems."""

        result = await self.external_system_repository.session.execute(
            select(ExternalSystem).where(ExternalSystem.is_active == True)  # noqa: E712
        )
        return [self._to_external_system_response(s) for s in result.scalars().all()]

    async def update_external_system(
        self, system_id: int, data: ExternalSystemUpdateRequest
    ) -> ExternalSystemResponse:
        """Update an external system."""
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
