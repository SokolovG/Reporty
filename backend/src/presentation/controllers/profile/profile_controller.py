from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, Request, delete, get, patch, post

from backend.src.application.dto.auth import UpdateUserData
from backend.src.application.dto.settings import (
    AIPreferencesUpdateData,
    AIProviderUpdateData,
    TaskTypeData,
    TaskTypeUpdateData,
)
from backend.src.application.use_cases.ai.ai_preferences_use_cases import AIPreferencesUseCases
from backend.src.application.use_cases.auth.user_use_cases import UserUseCases
from backend.src.application.use_cases.settings.settings_use_cases import SettingsUseCases
from backend.src.application.use_cases.tasks.task_type_use_cases import TaskTypeUseCases
from backend.src.infrastructure.database.mappers import Converter
from backend.src.presentation.dto import (
    TaskTypeResponse,
    UserResponse,
)
from backend.src.presentation.dto.auth.dto_classes import UserUpdateRequestDTO
from backend.src.presentation.dto.settings import (
    AIPreferencesUpdateRequestDTO,
    AIProviderUpdateRequestDTO,
    TaskTypeRequestDTO,
    TaskTypeUpdateRequestDTO,
)
from backend.src.presentation.dto.settings.responses import (
    AIModelResponse,
    AIPreferencesResponse,
    AIProviderResponse,
)
from backend.src.presentation.responses.base_responses import SuccessResponse, SuccessResponseDTO


class ProfileController(Controller):
    """Controller for user profile management - everything related to user's personal settings."""

    @patch("/user", dto=UserUpdateRequestDTO, return_dto=SuccessResponseDTO)
    @inject
    async def update_user_info(
        self,
        request: Request,
        data: UpdateUserData,
        converter: FromDishka[Converter],
        user_use_cases: FromDishka[UserUseCases],
    ) -> SuccessResponse:
        """Update user profile information."""
        user_id = request.user.id
        user = await user_use_cases.update(user_id=user_id, data=data)
        updated_user = converter.convert(user, UserResponse)
        return SuccessResponse(message="User updated successfully", data=updated_user)

    @patch("/ai-preferences", dto=AIPreferencesUpdateRequestDTO, return_dto=SuccessResponseDTO)
    @inject
    async def update_ai_preferences(
        self,
        request: Request,
        data: AIPreferencesUpdateData,
        ai_preferences_use_cases: FromDishka[AIPreferencesUseCases],
        converter: FromDishka[Converter],
    ) -> SuccessResponse:
        """Update user's AI preferences (provider selection, auto-processing)."""
        user_id = request.user.id
        updated_user = await ai_preferences_use_cases.update_user_preferences(
            user_id=user_id, data=data
        )
        result = AIPreferencesResponse(
            ai_auto_process=updated_user.ai_auto_process,
            ai_provider_id=updated_user.ai_provider_id,
        )
        return SuccessResponse(message="AI preferences updated successfully", data=result)

    @get("/ai-preferences/providers", return_dto=SuccessResponseDTO)
    @inject
    async def get_available_ai_providers(
        self,
        request: Request,
        ai_preferences_use_cases: FromDishka[AIPreferencesUseCases],
        converter: FromDishka[Converter],
    ) -> SuccessResponse:
        """Get available AI providers for user selection."""
        user_id = request.user.id
        providers = await ai_preferences_use_cases.get_active_providers(user_id=user_id)
        result = [
            AIProviderResponse(
                id=provider.id,
                name=provider.name,
                requires_api_key=provider.requires_api_key,
                is_active=provider.is_active,
                is_key_set=False,  # TODO: проверить есть ли ключ у юзера
                models=[AIModelResponse(id=m.id, name=m.name) for m in provider.models],
            )
            for provider in providers
        ]

        return SuccessResponse(data=result)

    @get("/task-types", return_dto=SuccessResponseDTO)
    @inject
    async def get_task_types(
        self,
        request: Request,
        settings_use_cases: FromDishka[SettingsUseCases],
        task_types_use_case: FromDishka[TaskTypeUseCases],
        converter: FromDishka[Converter],
    ) -> SuccessResponse:
        """Get user's task types."""
        user_id = request.user.id
        task_types_models = await task_types_use_case.get_many(user_id=user_id)

        result = [converter.convert(tt, TaskTypeResponse) for tt in task_types_models]
        return SuccessResponse(message="Task types retrieved successfully", data=result)

    @post("/task-types", dto=TaskTypeRequestDTO, return_dto=SuccessResponseDTO)
    @inject
    async def create_task_type(
        self,
        request: Request,
        data: TaskTypeData,
        settings_use_cases: FromDishka[SettingsUseCases],
        task_types_use_case: FromDishka[TaskTypeUseCases],
        converter: FromDishka[Converter],
    ) -> SuccessResponse:
        """Create new task type for user."""
        user_id = request.user.id
        task_type = await task_types_use_case.create(user_id=user_id, data=data)

        result = converter.convert(task_type, TaskTypeResponse)
        return SuccessResponse(message="Task type created successfully", data=result)

    @patch(
        "/task-types/{task_type_id:int}",
        dto=TaskTypeUpdateRequestDTO,
        return_dto=SuccessResponseDTO,
    )
    @inject
    async def update_task_type(
        self,
        request: Request,
        task_type_id: int,
        data: TaskTypeUpdateData,
        settings_use_cases: FromDishka[SettingsUseCases],
        task_types_use_case: FromDishka[TaskTypeUseCases],
        converter: FromDishka[Converter],
    ) -> SuccessResponse:
        """Update user's task type."""
        user_id = request.user.id
        task_type = await task_types_use_case.update(
            task_type_id=task_type_id, data=data, user_id=user_id
        )

        result = converter.convert(task_type, TaskTypeResponse)
        return SuccessResponse(message="Task type updated successfully", data=result)

    @delete("/task-types/{task_type_id:int}")
    @inject
    async def delete_task_type(
        self,
        request: Request,
        task_type_id: int,
        task_types_use_case: FromDishka[TaskTypeUseCases],
    ) -> None:
        """Delete user's task type."""
        user_id = request.user.id
        await task_types_use_case.delete(task_type_id=task_type_id, user_id=user_id)

    @patch(
        "/ai-preferences/providers/{ai_provider_id:int}",
        dto=AIProviderUpdateRequestDTO,
        return_dto=SuccessResponseDTO,
    )
    @inject
    async def update_ai_provider(
        self,
        request: Request,
        ai_provider_id: int,
        data: AIProviderUpdateData,
        settings_use_cases: FromDishka[SettingsUseCases],
        ai_preferences_use_case: FromDishka[AIPreferencesUseCases],
        converter: FromDishka[Converter],
    ) -> SuccessResponse:
        """Update AI provider configuration (admin only)."""
        user_id = request.user.id
        updated_user = await ai_preferences_use_case.update_provider(
            ai_provider_id=ai_provider_id, data=data, user_id=user_id
        )
        result = AIPreferencesResponse(
            ai_auto_process=updated_user.ai_auto_process,
            ai_provider_id=updated_user.ai_provider_id,
        )
        return SuccessResponse(message="AI provider updated successfully", data=result)
