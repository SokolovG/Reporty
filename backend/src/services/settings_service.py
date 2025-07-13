from adaptix.conversion import get_converter
from backend.src.database.repositories import (
    TaskTypeRepository,
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
        task_type_repository: TaskTypeRepository,
        ai_provider_repository: AIProviderRepository,
        user_profile_repository: UserProfileRepository,
        external_system_repository: ExternalSystemRepository,
    ) -> None:
        self.task_type_repository = task_type_repository
        self.ai_provider_repository = ai_provider_repository
        self.user_profile_repository = user_profile_repository
        self.external_system_repository = external_system_repository
        self._to_task_type_response = get_converter(TaskType, TaskTypeResponse)
        self._to_ai_provider_response = get_converter(AIProvider, AIProviderResponse)
        self._to_user_profile_response = get_converter(UserProfile, UserProfileResponse)
        self._to_external_system_response = get_converter(ExternalSystem, ExternalSystemResponse)

    # TaskType methods
    async def get_task_types(self, user_id: int) -> list[TaskTypeResponse]:
        user_profile = await self.user_profile_repository.get_by_user_id(user_id)
        return [self._to_task_type_response(task_type) for task_type in user_profile.task_types]

    async def create_task_type(self, user_id: int, data: TaskTypeRequest) -> TaskTypeResponse:
        user_profile = await self.user_profile_repository.get_by_user_id(user_id)
        task_type = TaskType(
            user_profile_id=user_profile.id,
            title=data.title,
            color=data.color,
        )
        added_task_type = await self.task_type_repository.add(task_type)
        await self.task_type_repository.session.commit()
        return self._to_task_type_response(added_task_type)

    async def update_task_type(
        self, task_type_id: int, data: TaskTypeUpdateRequest
    ) -> TaskTypeResponse:
        task_type = await self.task_type_repository.get(task_type_id)
        if data.title is not None:
            task_type.title = data.title
        if data.color is not None:
            task_type.color = data.color
        if data.is_active is not None:
            task_type.is_active = data.is_active
        updated_task_type = await self.task_type_repository.update(task_type)
        await self.task_type_repository.session.commit()
        return self._to_task_type_response(updated_task_type)

    async def delete_task_type(self, task_type_id: int) -> None:
        task_type = await self.task_type_repository.get(task_type_id)
        await self.task_type_repository.delete(task_type)
        await self.task_type_repository.session.commit()

    # AIProvider methods
    async def get_ai_providers(self) -> list[AIProviderResponse]:
        from sqlalchemy import select

        result = await self.ai_provider_repository.session.execute(select(AIProvider))
        return [self._to_ai_provider_response(p) for p in result.scalars().all()]

    async def get_active_ai_providers(self) -> list[AIProviderResponse]:
        from sqlalchemy import select

        result = await self.ai_provider_repository.session.execute(
            select(AIProvider).where(AIProvider.is_active == True)  # noqa: E712
        )
        return [self._to_ai_provider_response(p) for p in result.scalars().all()]

    async def update_ai_provider(
        self, ai_provider_id: int, data: AIProviderUpdateRequest
    ) -> AIProviderResponse:
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
        profile = await self.user_profile_repository.get_by_user_id(user_id)
        return self._to_user_profile_response(profile)

    async def update_user_profile(
        self, user_id: int, data: UserProfileUpdateRequest
    ) -> UserProfileResponse:
        profile = await self.user_profile_repository.get_by_user_id(user_id)
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
        from sqlalchemy import select

        result = await self.external_system_repository.session.execute(select(ExternalSystem))
        return [self._to_external_system_response(s) for s in result.scalars().all()]

    async def get_active_external_systems(self) -> list[ExternalSystemResponse]:
        from sqlalchemy import select

        result = await self.external_system_repository.session.execute(
            select(ExternalSystem).where(ExternalSystem.is_active == True)  # noqa: E712
        )
        return [self._to_external_system_response(s) for s in result.scalars().all()]

    async def update_external_system(
        self, system_id: int, data: ExternalSystemUpdateRequest
    ) -> ExternalSystemResponse:
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
