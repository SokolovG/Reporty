from datetime import datetime, timezone
from sqlalchemy import select

from backend.src.core.exceptions import NotFoundError, InternalServerError
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


class TaskService:
    def __init__(
        self,
        external_task_repo: ExternalTaskRepository,
        external_system_repo: ExternalSystemRepository,
    ):
        self.external_task_repo = external_task_repo
        self.external_system_repo = external_system_repo

    async def create_external_task(
        self, data: ExternalTaskCreateRequest, user_id: int
    ) -> ExternalTaskResponse:
        """Create a new external task."""
        try:
            result = await self.external_system_repo.session.execute(
                select(self.external_system_repo.model_type).where(
                    self.external_system_repo.model_type.name == "manual"
                )
            )
            system = result.scalar_one_or_none()

            if not system:
                raise NotFoundError(
                    "External system 'manual'",
                    details={"system_name": "manual", "help": "Create system via admin panel"},
                )

            now = datetime.now(timezone.utc)
            task = ExternalTask(
                external_id=data.external_id if data.external_id is not None else None,
                external_system_id=system.id,
                title=data.title,
                status="OPEN",
                url=data.url,
                external_created_at=now,
                user_id=user_id,
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
                user_id=user_id,
            )
        except Exception as e:
            if isinstance(e, (NotFoundError,)):
                raise
            raise InternalServerError(f"Failed to create task: {str(e)}", {"error": str(e)})

    async def update_external_task(
        self, task_id: int, data: ExternalTaskUpdateRequest, user_id: int
    ) -> ExternalTaskResponse:
        """Update an external task."""
        try:
            task = await self.external_task_repo.get_task(system_id=task_id, user_id=user_id)
        except Exception as e:
            raise InternalServerError(f"Failed to get task: {str(e)}", {"task_id": task_id})

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
        except Exception as e:
            raise InternalServerError(
                f"Failed to update task: {str(e)}", {"task_id": task_id, "error": str(e)}
            )

    async def delete_external_task(self, task_id: int, user_id: int) -> None:
        """Delete an external task."""
        try:
            task = await self.external_task_repo.get_task(system_id=task_id, user_id=user_id)
        except Exception as e:
            raise InternalServerError(f"Failed to get task: {str(e)}", {"task_id": task_id})

        try:
            await self.external_task_repo.session.delete(task)
            await self.external_task_repo.session.commit()
        except Exception as e:
            raise InternalServerError(
                f"Failed to delete task: {str(e)}", {"task_id": task_id, "error": str(e)}
            )
