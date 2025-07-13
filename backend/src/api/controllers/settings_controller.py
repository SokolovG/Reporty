from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get, post, patch, delete, Request

from backend.src.api.dto import (
    TaskTypeResponse,
    TaskTypeRequest,
    TaskTypeUpdateRequest,
    TaskTypeResponseDTO,
    TaskTypeRequestDTO,
    TaskTypeUpdateRequestDTO,
)
from backend.src.services.settings_service import SettingsService


class SettingsController(Controller):
    @get("/task-types", return_dto=TaskTypeResponseDTO)
    @inject
    async def get_task_types(
        self,
        request: Request,
        settings_service: FromDishka[SettingsService],
    ) -> list[TaskTypeResponse]:
        user_id = request.user.id
        task_types = await settings_service.get_task_types(user_id)
        return task_types

    @post("/task-types", dto=TaskTypeRequestDTO, return_dto=TaskTypeResponseDTO)
    @inject
    async def create_task_type(
        self,
        data: TaskTypeRequest,
        request: Request,
        settings_service: FromDishka[SettingsService],
    ) -> TaskTypeResponse:
        user_id = request.user.id
        task_type = await settings_service.create_task_type(user_id, data)
        return task_type

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
    ) -> TaskTypeResponse:
        task_type = await settings_service.update_task_type(task_type_id, data)
        return task_type

    @delete("/task-types/{task_type_id:int}")
    @inject
    async def delete_task_type(
        self,
        task_type_id: int,
        request: Request,
        settings_service: FromDishka[SettingsService],
    ) -> None:
        await settings_service.delete_task_type(task_type_id)
