from collections.abc import Sequence

from advanced_alchemy import repository
from sqlalchemy import and_, select

from backend.src.infrastructure.database.models import ExternalTaskModel
from backend.src.infrastructure.exceptions.api_exceptions import NotFoundError


class ExternalTaskRepository(repository.SQLAlchemyAsyncRepository[ExternalTaskModel]):  # ty: ignore
    """Repository for managing external tasks."""

    model_type: type[ExternalTaskModel] = ExternalTaskModel

    async def get_by_external_id(
        self, system_id: int, external_id: int, user_id: int
    ) -> ExternalTaskModel | None:
        """Get a task by external system and external ID."""
        result = await self.session.execute(
            select(ExternalTaskModel)
            .where(
                and_(
                    ExternalTaskModel.external_system_id == system_id,
                    ExternalTaskModel.external_id == external_id,
                )
            )
            .where(ExternalTaskModel.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_tasks_for_sync(self, system_id: int) -> Sequence[ExternalTaskModel]:
        """Get tasks that need synchronization."""
        result = await self.session.execute(
            select(ExternalTaskModel)
            .where(ExternalTaskModel.external_system_id == system_id)
            .order_by(ExternalTaskModel.last_sync.asc())
        )
        # TODO: daily record load and check user id
        return result.scalars().all()

    async def get_task(self, system_id: int, user_id: int) -> ExternalTaskModel:
        query = await self.session.execute(
            select(ExternalTaskModel)
            .where(ExternalTaskModel.id == system_id)
            .where(ExternalTaskModel.user_id == user_id)
        )

        task = query.scalar_one_or_none()
        if not task:
            raise NotFoundError("External task", system_id)
        return task
