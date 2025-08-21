from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from backend.src.database.repositories.external_task_repository import (
    ExternalTaskRepository,
)
from backend.src.database.repositories.settings_repository import (
    ExternalSystemRepository,
)
from backend.src.database.models import ExternalTask
from backend.src.api.dto.record_dto import (
    ExternalTaskCreateRequest,
    ExternalTaskUpdateRequest,
    ExternalTaskResponse,
)
from backend.src.api.responses import ErrorResponse


class TaskService:
    def __init__(
        self,
        external_task_repo: ExternalTaskRepository,
        external_system_repo: ExternalSystemRepository,
    ):
        self.external_task_repo = external_task_repo
        self.external_system_repo = external_system_repo

    async def create_external_task(
        self, data: ExternalTaskCreateRequest
    ) -> ExternalTaskResponse | ErrorResponse:
        try:
            result = await self.external_system_repo.session.execute(
                select(self.external_system_repo.model_type).where(
                    self.external_system_repo.model_type.name == "manual"
                )
            )
            system = result.scalar_one_or_none()
            # if not system:
            #     return create_error(
            #         "EXTERNAL_SYSTEM_NOT_FOUND",
            #         "External system 'manual' not found",
            #         "Please create external system via migration or admin panel",
            #         {"system_name": "manual"},
            #     )

            now = datetime.now(timezone.utc)
            task = ExternalTask(
                external_id=data.external_id if data.external_id is not None else None,
                external_system_id=system.id,
                title=data.title,
                status="OPEN",
                url=data.url,
                external_created_at=now,
            )
            self.external_task_repo.session.add(task)
            await self.external_task_repo.session.commit()
            await self.external_task_repo.session.refresh(task)

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
        except Exception:
            pass
            # return internal_error(f"Failed to create task: {str(e)}", {"error": str(e)})

    async def update_external_task(
        self, task_id: int, data: ExternalTaskUpdateRequest
    ) -> ExternalTaskResponse | ErrorResponse:
        try:
            task = await self.external_task_repo.get(task_id)
        except NoResultFound:
            pass

        try:
            if data.url is not None:
                task.url = data.url
            if data.title is not None:
                task.title = data.title
            if data.external_id is not None:
                task.external_id = data.external_id
            if data.status is not None:
                task.status = data.status
            if data.description is not None:
                task.description = data.description
            await self.external_task_repo.session.commit()
            await self.external_task_repo.session.refresh(task)

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
        except Exception:
            pass
            # return internal_error(
            #     f"Failed to update task: {str(e)}", {"task_id": task_id, "error": str(e)}
            # )

    async def delete_external_task(self, task_id: int) -> None | ErrorResponse:
        try:
            task = await self.external_task_repo.get(task_id)
        except NoResultFound:
            pass
            # return not_found_error("Task", task_id)

        try:
            await self.external_task_repo.session.delete(task)
            await self.external_task_repo.session.commit()
            return None
        except Exception:
            pass
            # return internal_error(
            #     f"Failed to delete task: {str(e)}", {"task_id": task_id, "error": str(e)}
            # )
