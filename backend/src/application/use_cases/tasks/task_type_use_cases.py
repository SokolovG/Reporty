from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.src.infrastructure.database.models import TaskType, User
from backend.src.infrastructure.database.repositories import (
    ExternalSystemRepository,
    ExternalTaskRepository,
    UserRepository,
)
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError, NotFoundError
from backend.src.presentation.dto import TaskTypeRequest, TaskTypeResponse, TaskTypeUpdateRequest
from backend.src.presentation.dto.converters import task_type_to_response


class TaskTypeUseCases:
    def __init__(
        self,
        external_task_repo: ExternalTaskRepository,
        external_system_repo: ExternalSystemRepository,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository
        self.external_task_repo = external_task_repo
        self.external_system_repo = external_system_repo

    async def get_many(self, user_id: int) -> list[TaskTypeResponse]:
        """Get all task types for a user."""
        try:
            result = await self.user_repository.session.execute(
                select(User).options(selectinload(User.task_types)).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                return []

            return [task_type_to_response(task_type) for task_type in user.task_types]
        except Exception as e:
            raise InternalServerError(f"Failed to get task types: {str(e)}", {"user_id": user_id})

    async def create(self, user_id: int, data: TaskTypeRequest) -> TaskTypeResponse:
        """Create a new task type for a user."""
        try:
            result = await self.user_repository.session.execute(
                select(User).options(selectinload(User.task_types)).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                raise NotFoundError("User", details={"user_id": user_id})

            task_type = TaskType(
                user_id=user.id,
                title=data.title,
                color=data.color,
            )
            user.task_types.append(task_type)
            await self.user_repository.session.commit()
            return task_type_to_response(task_type)
        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(f"Failed to create task type: {str(e)}", {"user_id": user_id})

    async def update(
        self, task_type_id: int, data: TaskTypeUpdateRequest, user_id: int
    ) -> TaskTypeResponse:
        """Update an existing task type."""
        try:
            result = await self.user_repository.session.execute(
                select(User)
                .options(selectinload(User.task_types))
                .join(TaskType, User.id == TaskType.user_id)
                .where(TaskType.id == task_type_id)
                .where(User.id == user_id)
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
            return task_type_to_response(task_type)
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
                select(User)
                .options(selectinload(User.task_types))
                .join(TaskType, User.id == TaskType.user_id)
                .where(TaskType.id == task_type_id)
                .where(User.id == user_id)
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
