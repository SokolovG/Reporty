from collections.abc import Sequence
from advanced_alchemy import repository
from sqlalchemy import select

from backend.src.domain.entities.task_type import TaskType
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.models import TaskTypeModel
from backend.src.infrastructure.exceptions.api_exceptions import NotFoundError


class TaskTypeRepository(repository.SQLAlchemyAsyncRepository[TaskTypeModel]):  # type: ignore[misc]
    """Repository for TaskType operations."""

    model_type: type[TaskTypeModel] = TaskTypeModel

    def __init__(self, converter: Converter, **kwargs) -> None:
        super().__init__(**kwargs)
        self.converter = converter

    async def get_all_for_user(self, user_id: int) -> Sequence[TaskType]:
        """Get all task types for a specific user."""
        result = await self.session.execute(
            select(TaskTypeModel)
            .where(TaskTypeModel.user_id == user_id)
            .order_by(TaskTypeModel.title)
        )
        models = result.scalars().all()
        return self.converter.convert_list(list(models), TaskType)

    async def get_by_id_and_user(self, task_type_id: int, user_id: int) -> TaskType:
        """Get a specific task type for a user."""
        model = await self.get_model_by_id_and_user(task_type_id, user_id)
        return self.converter.convert(model, TaskType)

    async def get_model_by_id_and_user(self, task_type_id: int, user_id: int) -> TaskTypeModel:
        result = await self.session.execute(
            select(TaskTypeModel)
            .where(TaskTypeModel.id == task_type_id)
            .where(TaskTypeModel.user_id == user_id)
        )
        task_type = result.scalar_one_or_none()
        if not task_type:
            raise NotFoundError("TaskType", task_type_id)
        return task_type

    async def create_for_user(self, user_id: int, title: str, color: str | None = None) -> TaskType:
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
        return self.converter.convert(created, TaskType)

    async def delete_task_type(self, task_type_id: int) -> None:
        """Delete a task type and commit."""
        await self.delete(task_type_id)
        await self.session.commit()

    async def update_task_type(
        self,
        task_type_id: int,
        user_id: int,
        title: str | None = None,
        color: str | None = None,
        is_active: bool | None = None,
    ) -> TaskType:
        """Update an existing task type."""
        model = await self.get_model_by_id_and_user(task_type_id, user_id)

        if title is not None:
            model.title = title
        if color is not None:
            model.color = color
        if is_active is not None:
            model.is_active = is_active

        await self.session.commit()
        await self.session.refresh(model)
        return self.converter.convert(model, TaskType)
