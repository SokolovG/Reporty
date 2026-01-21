from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.src.domain.entities.task_type import TaskType
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.models import TaskTypeModel, UserModel
from backend.src.infrastructure.database.repositories import (
    ExternalSystemRepository,
    ExternalTaskRepository,
    UserRepository,
)
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError, NotFoundError
from backend.src.presentation.dto import TaskTypeRequest, TaskTypeUpdateRequest


class TaskTypeUseCases:
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

    async def get_many(self, user_id: int) -> list[TaskType]:
        """Get all task types for a user."""
        try:
            result = await self.user_repository.session.execute(
                select(UserModel)
                .options(selectinload(UserModel.task_types))
                .where(UserModel.id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                return []

            return [self.converter.convert(tt, TaskType) for tt in user.task_types]
        except Exception as e:
            raise InternalServerError(f"Failed to get task types: {str(e)}", {"user_id": user_id})

    async def create(self, user_id: int, data: TaskTypeRequest) -> TaskType:
        """Create a new task type for a user."""
        try:
            result = await self.user_repository.session.execute(
                select(UserModel)
                .options(selectinload(UserModel.task_types))
                .where(UserModel.id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                raise NotFoundError("User", details={"user_id": user_id})

            task_type = TaskTypeModel(
                user_id=user.id,
                title=data.title,
                color=data.color,
            )
            user.task_types.append(task_type)
            await self.user_repository.session.commit()
            return self.converter.convert(task_type, TaskType)

        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(f"Failed to create task type: {str(e)}", {"user_id": user_id})

    async def update(
        self, task_type_id: int, data: TaskTypeUpdateRequest, user_id: int
    ) -> TaskType:
        """Update an existing task type."""
        try:
            result = await self.user_repository.session.execute(
                select(UserModel)
                .options(selectinload(UserModel.task_types))
                .join(TaskTypeModel, UserModel.id == TaskTypeModel.user_id)
                .where(TaskTypeModel.id == task_type_id)
                .where(UserModel.id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                raise NotFoundError("TaskType", task_type_id)

            task_type = next((tt for tt in user.task_types if tt.id == task_type_id), None)
            if not task_type:
                raise NotFoundError("TaskType", task_type_id)

            if data.title is not None:
                task_type.title = data.title
            if data.color is not None:
                task_type.color = data.color
            if data.is_active is not None:
                task_type.is_active = data.is_active

            await self.user_repository.session.commit()
            return self.converter.convert(task_type, TaskType)

        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(
                f"Failed to update task type: {str(e)}", {"task_type_id": task_type_id}
            )

    async def delete(self, task_type_id: int, user_id: int) -> None:
        """Delete a task type."""
        try:
            result = await self.user_repository.session.execute(
                select(UserModel)
                .options(selectinload(UserModel.task_types))
                .join(TaskTypeModel, UserModel.id == TaskTypeModel.user_id)
                .where(TaskTypeModel.id == task_type_id)
                .where(UserModel.id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                raise NotFoundError("TaskType", task_type_id)

            task_type = next((tt for tt in user.task_types if tt.id == task_type_id), None)
            if not task_type:
                raise NotFoundError("TaskType", task_type_id)

            user.task_types.remove(task_type)
            await self.user_repository.session.commit()
        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(
                f"Failed to delete task type: {str(e)}", {"task_type_id": task_type_id}
            )
