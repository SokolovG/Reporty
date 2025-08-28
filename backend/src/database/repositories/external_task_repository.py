from collections.abc import Sequence

from advanced_alchemy import repository
from sqlalchemy import and_, select

from backend.src.core.exceptions import NotFoundError
from backend.src.database.models import ExternalTask


class ExternalTaskRepository(repository.SQLAlchemyAsyncRepository[ExternalTask]):  # type: ignore
    """Repository for managing external tasks."""

    model_type: type[ExternalTask] = ExternalTask

    async def get_by_external_id(
        self, system_id: int, external_id: int, user_id: int
    ) -> ExternalTask:
        """Get a task by external system and external ID."""
        result = await self.session.execute(
            select(ExternalTask).where(
                and_(
                    ExternalTask.external_system_id == system_id,
                    ExternalTask.external_id == external_id,
                )
            )
            # TODO: daily record load and check user id
        )
        return result.scalar_one_or_none()

    async def get_tasks_for_sync(self, system_id: int) -> Sequence[ExternalTask]:
        """Get tasks that need synchronization."""
        result = await self.session.execute(
            select(ExternalTask)
            .where(ExternalTask.external_system_id == system_id)
            .order_by(ExternalTask.last_sync.asc())
        )
        # TODO: daily record load and check user id
        return result.scalars().all()

    async def get_task(self, system_id: int, user_id: int) -> ExternalTask:
        query = await self.session.execute(
            select(ExternalTask)
            .where(ExternalTask.id == system_id)
            .where(ExternalTask.user_id == user_id)
        )

        task = query.one_or_none()
        if not task:
            raise NotFoundError("External task", system_id)
        return task
