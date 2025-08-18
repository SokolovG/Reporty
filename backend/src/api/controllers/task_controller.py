from litestar import Controller, post, put, delete
from backend.src.api.dto.record_dto import (
    ExternalTaskCreateRequest,
    ExternalTaskCreateRequestDTO,
    ExternalTaskUpdateRequest,
    ExternalTaskUpdateRequestDTO,
    ExternalTaskResponse,
    ExternalTaskResponseDTO,
)
from backend.src.api.decorators import crud_error_handler
from backend.src.services.task_service import TaskService
from dishka.integrations.litestar import inject
from dishka import FromDishka


class TaskController(Controller):
    @post("/external-tasks/", dto=ExternalTaskCreateRequestDTO, return_dto=ExternalTaskResponseDTO)
    @crud_error_handler
    @inject
    async def create_external_task(
        self, data: ExternalTaskCreateRequest, task_service: FromDishka[TaskService]
    ) -> ExternalTaskResponse:
        return await task_service.create_external_task(data)

    @put(
        "/external-tasks/{task_id:int}",
        dto=ExternalTaskUpdateRequestDTO,
        return_dto=ExternalTaskResponseDTO,
    )
    @crud_error_handler
    @inject
    async def update_external_task(
        self,
        task_id: int,
        data: ExternalTaskUpdateRequest,
        task_service: FromDishka[TaskService],
    ) -> ExternalTaskResponse:
        return await task_service.update_external_task(task_id, data)

    @delete("/external-tasks/{task_id:int}", status_code=204)
    @crud_error_handler
    @inject
    async def delete_external_task(
        self, task_id: int, task_service: FromDishka[TaskService]
    ) -> None:
        return await task_service.delete_external_task(task_id)
