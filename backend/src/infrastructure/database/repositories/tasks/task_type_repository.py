from advanced_alchemy import repository
from sqlalchemy import select

from backend.src.infrastructure.database.models import TaskTypeModel
from backend.src.infrastructure.exceptions.api_exceptions import NotFoundError


class TaskTypeRepository(repository.SQLAlchemyAsyncRepository[TaskTypeModel]):  # type: ignore[misc]
    """Repository for TaskType operations."""

    model_type: type[TaskTypeModel] = TaskTypeModel

    async def get_all_for_user(self, user_id: int) -> list[TaskTypeModel]:
        """Get all task types for a specific user.

        Args:
            user_id: ID of the user

        Returns:
            List of task type models
        """
        result = await self.session.execute(
            select(TaskTypeModel)
            .where(TaskTypeModel.user_id == user_id)
            .order_by(TaskTypeModel.title)
        )
        return list(result.scalars().all())

    async def get_by_id_and_user(self, task_type_id: int, user_id: int) -> TaskTypeModel:
        """Get a specific task type for a user.

        Args:
            task_type_id: ID of the task type
            user_id: ID of the user

        Returns:
            Task type model

        Raises:
            NotFoundError: If task type not found or doesn't belong to user
        """
        result = await self.session.execute(
            select(TaskTypeModel)
            .where(TaskTypeModel.id == task_type_id)
            .where(TaskTypeModel.user_id == user_id)
        )
        task_type = result.scalar_one_or_none()

        if not task_type:
            raise NotFoundError("TaskType", task_type_id)

        return task_type

    async def create_for_user(
        self, user_id: int, title: str, color: str | None = None
    ) -> TaskTypeModel:
        """Create a new task type for a user.

        Args:
            user_id: ID of the user
            title: Title of the task type
            color: Optional color for the task type

        Returns:
            Created task type model
        """
        task_type = TaskTypeModel(
            user_id=user_id,
            title=title,
            color=color,
        )
        created = await self.add(task_type)
        await self.session.commit()
        await self.session.refresh(created)
        return created
