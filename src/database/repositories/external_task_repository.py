from collections.abc import Sequence
from uuid import UUID

from advanced_alchemy import repository
from sqlalchemy import and_, select

from src.database.models import ExternalTask


class ExternalTaskRepository(repository.SQLAlchemyAsyncRepository[ExternalTask]):  # type: ignore
    """Repository for managing external tasks."""

    model_type: type[ExternalTask] = ExternalTask

    async def get_by_external_id(self, system_id: UUID, external_id: str) -> ExternalTask | None:
        """Get a task by external system and external ID."""
        result = await self.session.execute(
            select(ExternalTask).where(
                and_(
                    ExternalTask.external_system_id == system_id,
                    ExternalTask.external_id == external_id,
                )
            )
        )
        return result.scalar_one_or_none()

    async def get_tasks_for_sync(self, system_id: UUID) -> Sequence[ExternalTask]:
        """Get tasks that need synchronization."""
        result = await self.session.execute(
            select(ExternalTask)
            .where(ExternalTask.external_system_id == system_id)
            .order_by(ExternalTask.last_sync.asc())
        )
        return result.scalars().all()
