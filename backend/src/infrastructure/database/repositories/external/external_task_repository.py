from collections.abc import Sequence
from datetime import datetime
from advanced_alchemy import repository
from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload

from backend.src.application.dto.records import ExternalTaskCreateData
from backend.src.domain.entities import ExternalTask
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.models import ExternalTaskModel
from backend.src.infrastructure.exceptions.api_exceptions import NotFoundError


class ExternalTaskRepository(repository.SQLAlchemyAsyncRepository[ExternalTaskModel]):  # ty: ignore
    """Repository for managing external tasks."""

    model_type: type[ExternalTaskModel] = ExternalTaskModel

    def __init__(self, converter: Converter, **kwargs) -> None:
        super().__init__(**kwargs)
        self.converter = converter

    async def get_by_id(self, task_id: int, user_id: int) -> ExternalTask | None:
        """Get task by ID."""
        result = await self.session.execute(
            select(ExternalTaskModel)
            .where(ExternalTaskModel.id == task_id)
            .where(ExternalTaskModel.user_id == user_id)
            .options(selectinload(ExternalTaskModel.system))
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return self.converter.convert(model, ExternalTask)

    async def get_by_external_id(
        self, system_id: int, external_id: int, user_id: int
    ) -> ExternalTask | None:
        """Get a task by external system and external ID."""
        result = await self.session.execute(
            select(ExternalTaskModel)
            .where(
                and_(
                    ExternalTaskModel.external_system_id == system_id,
                    ExternalTaskModel.external_id == external_id,
                    ExternalTaskModel.user_id == user_id,
                )
            )
            .options(selectinload(ExternalTaskModel.system))
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return self.converter.convert(model, ExternalTask)

    async def create_task(
        self, data: ExternalTaskCreateData, user_id: int, system_id: int
    ) -> ExternalTask:
        """Create new external task."""
        task_model = ExternalTaskModel(
            user_id=user_id,
            external_id=data.external_id,
            external_system_id=system_id,
            title=data.title,
            description=data.description,
            status=data.status or "TODO",
            url=data.url or "",
            external_created_at=data.external_created_at or datetime.now(),
        )

        self.session.add(task_model)
        await self.session.commit()
        await self.session.refresh(task_model, attribute_names=["system"])

        return self.converter.convert(task_model, ExternalTask)

    async def update_task(self, task: ExternalTask) -> ExternalTask:
        """Update existing task."""
        result = await self.session.execute(
            select(ExternalTaskModel).where(ExternalTaskModel.id == task.id)
        )
        task_model = result.scalar_one_or_none()

        if not task_model:
            raise NotFoundError("ExternalTask", task.id)

        task_model.title = task.title
        task_model.description = task.description
        task_model.status = task.status
        task_model.url = task.url
        task_model.external_id = task.external_id
        task_model.external_updated_at = task.external_updated_at
        task_model.completed_at = task.completed_at

        await self.session.commit()
        await self.session.refresh(task_model, attribute_names=["system"])

        return self.converter.convert(task_model, ExternalTask)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        """Delete task."""
        result = await self.session.execute(
            select(ExternalTaskModel)
            .where(ExternalTaskModel.id == task_id)
            .where(ExternalTaskModel.user_id == user_id)
        )
        task_model = result.scalar_one_or_none()

        if not task_model:
            raise NotFoundError("ExternalTask", task_id)

        await self.session.delete(task_model)
        await self.session.commit()

    async def get_tasks_for_sync(self, system_id: int) -> Sequence[ExternalTask]:
        """Get tasks that need synchronization."""
        result = await self.session.execute(
            select(ExternalTaskModel)
            .where(ExternalTaskModel.external_system_id == system_id)
            .options(selectinload(ExternalTaskModel.system))
            .order_by(ExternalTaskModel.last_sync.asc())
        )
        models = list(result.scalars().all())
        return self.converter.convert_list(models, ExternalTask)
