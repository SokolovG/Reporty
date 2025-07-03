from litestar import Controller
from litestar import post
from litestar import put, delete
from backend.src.api.dto.record_dto import (
    ExternalTaskCreateRequest,
    ExternalTaskCreateRequestDTO,
    ExternalTaskUpdateRequest,
    ExternalTaskUpdateRequestDTO,
    ExternalTaskResponse,
    ExternalTaskResponseDTO,
)
from backend.src.services.task_service import TaskService
from dishka.integrations.litestar import inject
from dishka import FromDishka


class TaskController(Controller):
    @post(
        "/external-tasks/",
        dto=ExternalTaskCreateRequestDTO,
        return_dto=ExternalTaskResponseDTO,
    )
    @inject
    async def create_external_task(
        self, data: ExternalTaskCreateRequest, task_service: FromDishka[TaskService]
    ) -> ExternalTaskResponse:
        task = await task_service.create_external_task(data)
        return ExternalTaskResponse(
            id=task.id,
            external_id=task.external_id,
            external_system_id=task.external_system_id,
            title=task.title,
            description=task.description,
            status=task.status,
            url=task.url,
            external_created_at=task.external_created_at,
            external_updated_at=task.external_updated_at,
            completed_at=task.completed_at,
            last_sync=task.last_sync,
        )

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
    ) -> ExternalTaskResponse:
        task = await task_service.update_external_task(task_id, data)
        return ExternalTaskResponse(
            id=task.id,
            external_id=task.external_id,
            external_system_id=task.external_system_id,
            title=task.title,
            description=task.description,
            status=task.status,
            url=task.url,
            external_created_at=task.external_created_at,
            external_updated_at=task.external_updated_at,
            completed_at=task.completed_at,
            last_sync=task.last_sync,
        )

    @delete("/external-tasks/{task_id:int}", status_code=204)
    @inject
    async def delete_external_task(
        self, task_id: int, task_service: FromDishka[TaskService]
    ) -> None:
        await task_service.delete_external_task(task_id)
