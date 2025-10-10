from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get, post, patch, delete, Request

from backend.src.api.dto import (
    TaskTypeRequest,
    TaskTypeUpdateRequest,
    TaskTypeResponseDTO,
    TaskTypeRequestDTO,
    TaskTypeUpdateRequestDTO,
)
from backend.src.api.dto.auth_dto import UserResponseDTO, UserUpdateRequest
from backend.src.api.dto.settings_dto import AISettingsUpdateRequest, AISettingsUpdateRequestDTO, AISettingsUpdateResponseDTO
from backend.src.services.settings_service import SettingsService
from backend.src.api.responses.base_responses import SuccessResponse


class SettingsController(Controller):
    @get("/task-types", return_dto=TaskTypeResponseDTO)
    @inject
    async def get_task_types(
        self,
        request: Request,
        settings_service: FromDishka[SettingsService],
    ) -> SuccessResponse:
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
        user_id = request.user.id
        await settings_service.delete_task_type(task_type_id=task_type_id, user_id=user_id)

    @patch("/user", return_dto=UserResponseDTO)
    @inject
    async def update_user_info(
        self,
        data: UserUpdateRequest,
        request: Request,
        settings_service: FromDishka[SettingsService],
    ) -> SuccessResponse:
        user_id = request.user.id
        updated_user = await settings_service.update_user(user_id=user_id, data=data)
        return SuccessResponse(message="User updated successfully", data=updated_user)

    @patch("/ai_settings", dto=AISettingsUpdateRequestDTO,return_dto=AISettingsUpdateResponseDTO)
    @inject
    async def update_ai_settings(
        self,
        data: AISettingsUpdateRequest,
        request: Request,
        settings_service: FromDishka[SettingsService]
    ):
        user_id = request.user.id
        updates_ai_settings = await settings_service.update_ai_settings(user_id=user_id, data=data)
        return SuccessResponse(message="Ai settings updated successfully", data=updates_ai_settings)
