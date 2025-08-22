from litestar import Controller, post, put, delete
from backend.src.api.dto.record_dto import (
    ExternalTaskCreateRequest,
    ExternalTaskCreateRequestDTO,
    ExternalTaskUpdateRequest,
    ExternalTaskUpdateRequestDTO,
    ExternalTaskResponseDTO,
)
from backend.src.services.task_service import TaskService
from dishka.integrations.litestar import inject
from dishka import FromDishka
from backend.src.api.responses.base_responses import SuccessResponse


class TaskController(Controller):
    @post("/external-tasks/", dto=ExternalTaskCreateRequestDTO, return_dto=ExternalTaskResponseDTO)
    @inject
    async def create_external_task(
        self, data: ExternalTaskCreateRequest, task_service: FromDishka[TaskService]
    ) -> SuccessResponse:
        result = await task_service.create_external_task(data)
        return SuccessResponse(message="External task created successfully", data=result)

    @put(
        "/external-tasks/{task_id:int}",
        dto=ExternalTaskUpdateRequestDTO,
        return_dto=ExternalTaskResponseDTO,
    )
    @inject
    async def update_external_task(
        self,
        task_id: int,
        data: ExternalTaskUpdateRequest,
        task_service: FromDishka[TaskService],
    ) -> SuccessResponse:
        result = await task_service.update_external_task(task_id, data)
        return SuccessResponse(message="External task updated successfully", data=result)

    @delete("/external-tasks/{task_id:int}", status_code=204)
    @inject
    async def delete_external_task(
        self, task_id: int, task_service: FromDishka[TaskService]
    ) -> SuccessResponse:
        await task_service.delete_external_task(task_id)
        return SuccessResponse(message="External task deleted successfully")
