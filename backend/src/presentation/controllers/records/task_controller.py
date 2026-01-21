from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, Request, delete, post, put

from backend.src.application.use_cases.tasks.tasks_use_cases import TasksUseCase
from backend.src.presentation.dto.records import (
    ExternalTaskCreateRequest,
    ExternalTaskCreateRequestDTO,
    ExternalTaskUpdateRequest,
    ExternalTaskUpdateRequestDTO,
)
from backend.src.presentation.responses.base_responses import SuccessResponse, SuccessResponseDTO


class TaskController(Controller):
    @post("/external-tasks/", dto=ExternalTaskCreateRequestDTO, return_dto=SuccessResponseDTO)
    @inject
    async def create_external_task(
        self,
        data: ExternalTaskCreateRequest,
        task_use_casess: FromDishka[TasksUseCase],
        request: Request,
    ) -> SuccessResponse:
        """Create a new external task."""
        user_id = request.user.id
        result = await task_use_casess.create_external(data=data, user_id=user_id)
        return SuccessResponse(message="External task created successfully", data=result)

    @put(
        "/external-tasks/{task_id:int}",
        dto=ExternalTaskUpdateRequestDTO,
        return_dto=SuccessResponseDTO,
    )
    @inject
    async def update_external_task(
        self,
        task_id: int,
        data: ExternalTaskUpdateRequest,
        task_use_casess: FromDishka[TasksUseCase],
        request: Request,
    ) -> SuccessResponse:
        """Update an external task."""
        user_id = request.user.id
        result = await task_use_casess.update_external(task_id=task_id, data=data, user_id=user_id)
        return SuccessResponse(message="External task updated successfully", data=result)

    @delete("/external-tasks/{task_id:int}", status_code=204)
    @inject
    async def delete_external_task(
        self, task_id: int, task_use_casess: FromDishka[TasksUseCase], request: Request
    ) -> None:
        """Delete an external task."""
        user_id = request.user.id
        await task_use_casess.delete_external(task_id=task_id, user_id=user_id)
