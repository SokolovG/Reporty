from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get, post, patch, delete, Request

from backend.src.api.dto.auth_dto import UserResponseDTO, UserUpdateRequest
from backend.src.api.dto.settings_dto import (
    AIPreferencesUpdateRequest,
    AIPreferencesUpdateRequestDTO,
    AIPreferencesResponseDTO,
    AIProviderResponseDTO,
    AIProviderUpdateRequest,
    AIProviderUpdateRequestDTO,
    TaskTypeRequest,
    TaskTypeUpdateRequest,
    TaskTypeResponseDTO,
    TaskTypeRequestDTO,
    TaskTypeUpdateRequestDTO,
)
from backend.src.services.settings_service import SettingsService
from backend.src.api.responses.base_responses import SuccessResponse


class ProfileController(Controller):
    """Controller for user profile management - everything related to user's personal settings."""

    @patch("/user", return_dto=UserResponseDTO)
    @inject
    async def update_user_info(
        self,
        data: UserUpdateRequest,
        request: Request,
        settings_service: FromDishka[SettingsService],
    ) -> SuccessResponse:
        """Update user profile information."""
        user_id = request.user.id
        updated_user = await settings_service.update_user(user_id=user_id, data=data)
        return SuccessResponse(message="User updated successfully", data=updated_user)

    @patch(
        "/ai-preferences", dto=AIPreferencesUpdateRequestDTO, return_dto=AIPreferencesResponseDTO
    )
    @inject
    async def update_ai_preferences(
        self,
        data: AIPreferencesUpdateRequest,
        request: Request,
        settings_service: FromDishka[SettingsService],
    ) -> SuccessResponse:
        """Update user's AI preferences (provider selection, auto-processing)."""
        user_id = request.user.id
        updated_preferences = await settings_service.update_user_ai_preferences(
            user_id=user_id, data=data
        )
        return SuccessResponse(
            message="AI preferences updated successfully", data=updated_preferences
        )

    @get("/ai-preferences/providers", return_dto=AIProviderResponseDTO)
    @inject
    async def get_available_ai_providers(
        self, request: Request, settings_service: FromDishka[SettingsService]
    ) -> SuccessResponse:
        """Get available AI providers for user selection."""
        user_id = request.user.id
        providers = await settings_service.get_active_ai_providers(user_id=user_id)
        return SuccessResponse(
            message="Available AI providers retrieved successfully", data=providers
        )

    @get("/task-types", return_dto=TaskTypeResponseDTO)
    @inject
    async def get_task_types(
        self,
        request: Request,
        settings_service: FromDishka[SettingsService],
    ) -> SuccessResponse:
        """Get user's task types."""
        user_id = request.user.id
        task_types = await settings_service.get_task_types(user_id=user_id)
        return SuccessResponse(message="Task types retrieved successfully", data=task_types)

    @post("/task-types", dto=TaskTypeRequestDTO, return_dto=TaskTypeResponseDTO)
    @inject
    async def create_task_type(
        self,
        data: TaskTypeRequest,
        request: Request,
        settings_service: FromDishka[SettingsService],
    ) -> SuccessResponse:
        """Create new task type for user."""
        user_id = request.user.id
        task_type = await settings_service.create_task_type(user_id=user_id, data=data)
        return SuccessResponse(message="Task type created successfully", data=task_type)

    @patch(
        "/task-types/{task_type_id:int}",
        dto=TaskTypeUpdateRequestDTO,
        return_dto=TaskTypeResponseDTO,
    )
    @inject
    async def update_task_type(
        self,
        task_type_id: int,
        data: TaskTypeUpdateRequest,
        request: Request,
        settings_service: FromDishka[SettingsService],
    ) -> SuccessResponse:
        """Update user's task type."""
        user_id = request.user.id
        task_type = await settings_service.update_task_type(
            task_type_id=task_type_id, data=data, user_id=user_id
        )
        return SuccessResponse(message="Task type updated successfully", data=task_type)

    @delete("/task-types/{task_type_id:int}")
    @inject
    async def delete_task_type(
        self,
        task_type_id: int,
        request: Request,
        settings_service: FromDishka[SettingsService],
    ) -> None:
        """Delete user's task type."""
        user_id = request.user.id
        await settings_service.delete_task_type(task_type_id=task_type_id, user_id=user_id)

    @get("/ai-providers", return_dto=AIProviderResponseDTO)
    @inject
    async def get_all_ai_providers(
        self, request: Request, settings_service: FromDishka[SettingsService]
    ) -> SuccessResponse:
        """Get all AI providers (admin function)."""
        user_id = request.user.id
        providers = await settings_service.get_all_ai_providers(user_id=user_id)
        return SuccessResponse(message="All AI providers retrieved successfully", data=providers)

    @patch(
        "/ai-providers/{ai_provider_id:int}",
        dto=AIProviderUpdateRequestDTO,
        return_dto=AIProviderResponseDTO,
    )
    @inject
    async def update_ai_provider(
        self,
        ai_provider_id: int,
        data: AIProviderUpdateRequest,
        request: Request,
        settings_service: FromDishka[SettingsService],
    ) -> SuccessResponse:
        """Update AI provider configuration (admin only)."""
        updated_provider = await settings_service.update_ai_provider(
            ai_provider_id=ai_provider_id, data=data
        )
        return SuccessResponse(message="AI provider updated successfully", data=updated_provider)
