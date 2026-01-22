from datetime import datetime, timezone

from sqlalchemy import select

from backend.src.application.dto.records import ExternalTaskCreateData, ExternalTaskUpdateData
from backend.src.domain.entities.external_task import ExternalTask
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.models import ExternalTaskModel
from backend.src.infrastructure.database.repositories import (
    ExternalSystemRepository,
    ExternalTaskRepository,
    UserRepository,
)
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError, NotFoundError


class TasksUseCase:
    def __init__(
        self,
        external_task_repo: ExternalTaskRepository,
        external_system_repo: ExternalSystemRepository,
        user_repository: UserRepository,
        converter: Converter,
    ):
        self.user_repository = user_repository
        self.external_task_repo = external_task_repo
        self.external_system_repo = external_system_repo
        self.converter = converter

    async def create_external(self, data: ExternalTaskCreateData, user_id: int) -> ExternalTask:
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
            task = ExternalTaskModel(
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

            return self.converter.convert(task, ExternalTask)

        except Exception as e:
            if isinstance(e, (NotFoundError,)):
                raise
            raise InternalServerError(f"Failed to create task: {str(e)}", {"error": str(e)})

    async def update_external(
        self, task_id: int, data: ExternalTaskUpdateData, user_id: int
    ) -> ExternalTask:
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

            return self.converter.convert(task, ExternalTask)

        except Exception as e:
            raise InternalServerError(
                f"Failed to update task: {str(e)}", {"task_id": task_id, "error": str(e)}
            )

    async def delete_external(self, task_id: int, user_id: int) -> None:
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
