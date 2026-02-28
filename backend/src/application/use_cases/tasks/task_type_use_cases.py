from collections.abc import Sequence
from backend.src.application.dto.settings import TaskTypeData, TaskTypeUpdateData
from backend.src.application.ports.repositories import ITaskTypeRepository, IUserRepository
from backend.src.domain.entities.task_type import TaskType
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError, NotFoundError


class TaskTypeUseCases:
    """Use cases for task type management."""

    def __init__(
        self,
        task_type_repository: ITaskTypeRepository,
        user_repository: IUserRepository,
        converter: Converter,
    ) -> None:
        self.task_type_repository = task_type_repository
        self.user_repository = user_repository
        self.converter = converter

    async def get_many(self, user_id: int) -> Sequence[TaskType]:
        """Get all task types for a user.

        Args:
            user_id: ID of the user

        Returns:
            List of task type entities

        Raises:
            InternalServerError: If operation fails
        """
        try:
            return await self.task_type_repository.get_all_for_user(user_id)

        except Exception as e:
            raise InternalServerError(f"Failed to get task types: {str(e)}", {"user_id": user_id})

    async def create(self, user_id: int, data: TaskTypeData) -> TaskType:
        """Create a new task type for a user.

        Args:
            user_id: ID of the user
            data: Task type creation data

        Returns:
            Created task type entity

        Raises:
            NotFoundError: If user not found
            InternalServerError: If operation fails
        """
        try:
            user = await self.user_repository.get_one_or_none(id=user_id)
            if not user:
                raise NotFoundError("User", user_id)

            return await self.task_type_repository.create_for_user(
                user_id=user_id, title=data.title, color=data.color
            )

        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(f"Failed to create task type: {str(e)}", {"user_id": user_id})

    async def update(self, task_type_id: int, data: TaskTypeUpdateData, user_id: int) -> TaskType:
        """Update an existing task type.

        Args:
            task_type_id: ID of the task type to update
            data: Update data
            user_id: ID of the user (for authorization)

        Returns:
            Updated task type entity

        Raises:
            NotFoundError: If task type not found or doesn't belong to user
            InternalServerError: If operation fails
        """
        try:
            return await self.task_type_repository.update_task_type(
                task_type_id=task_type_id,
                user_id=user_id,
                title=data.title,
                color=data.color,
                is_active=data.is_active,
            )

        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(
                f"Failed to update task type: {str(e)}", {"task_type_id": task_type_id}
            )

    async def delete(self, task_type_id: int, user_id: int) -> None:
        """Delete a task type.

        Args:
            task_type_id: ID of the task type to delete
            user_id: ID of the user (for authorization)

        Raises:
            NotFoundError: If task type not found or doesn't belong to user
            InternalServerError: If operation fails
        """
        try:
            task_type_model = await self.task_type_repository.get_by_id_and_user(
                task_type_id, user_id
            )

            await self.task_type_repository.delete(task_type_model.id)
            await self.task_type_repository.session.commit()

        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(
                f"Failed to delete task type: {str(e)}", {"task_type_id": task_type_id}
            )
