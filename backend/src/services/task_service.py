from datetime import datetime, timezone
from sqlalchemy import select
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
)


class TaskService:
    def __init__(
        self,
        external_task_repo: ExternalTaskRepository,
        external_system_repo: ExternalSystemRepository,
    ):
        self.external_task_repo = external_task_repo
        self.external_system_repo = external_system_repo

    async def create_external_task(self, data: ExternalTaskCreateRequest) -> ExternalTask:
        result = await self.external_system_repo.session.execute(
            select(self.external_system_repo.model_type).where(
                self.external_system_repo.model_type.name == "manual"
            )
        )
        system = result.scalar_one_or_none()
        if not system:
            raise ValueError(
                "External system 'manual' not found. Please create it via migration or admin panel."
            )

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
        return task

    async def update_external_task(
        self, task_id: int, data: ExternalTaskUpdateRequest
    ) -> ExternalTask:
        task = await self.external_task_repo.get(task_id)
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
        return task

    async def delete_external_task(self, task_id: int) -> None:
        task = await self.external_task_repo.get(task_id)
        await self.external_task_repo.session.delete(task)
        await self.external_task_repo.session.commit()
