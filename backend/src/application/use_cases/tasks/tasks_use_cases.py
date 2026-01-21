from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.src.infrastructure.database.models import ExternalTask, TaskType, User
from backend.src.infrastructure.database.repositories import (
    ExternalSystemRepository,
    ExternalTaskRepository,
    UserRepository,
)
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError, NotFoundError
from backend.src.presentation.dto import (
    ExternalTaskCreateRequest,
    ExternalTaskResponse,
    ExternalTaskUpdateRequest,
    TaskTypeRequest,
    TaskTypeResponse,
    TaskTypeUpdateRequest,
)
from backend.src.presentation.dto.converters import task_type_to_response


class TasksUseCase:
    def __init__(
        self,
        external_task_repo: ExternalTaskRepository,
        external_system_repo: ExternalSystemRepository,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository
        self.external_task_repo = external_task_repo
        self.external_system_repo = external_system_repo

    async def create_external(
        self, data: ExternalTaskCreateRequest, user_id: int
    ) -> ExternalTaskResponse:
        """Create a new external task."""
        try:
            result = await self.external_system_repo.session.execute(
                select(self.external_system_repo.model_type).where(
                    self.external_system_repo.model_type.name == "manual"
                )
            )
            system = result.scalar_one_or_none()

            if not system:
                raise NotFoundError(
                    "External system 'manual'",
                    details={"system_name": "manual", "help": "Create system via admin panel"},
                )

            now = datetime.now(timezone.utc)
            task = ExternalTask(
                external_id=data.external_id if data.external_id is not None else None,
                external_system_id=system.id,
                title=data.title,
                status="OPEN",
                url=data.url,
                external_created_at=now,
                user_id=user_id,
            )

            self.external_task_repo.session.add(task)
            await self.external_task_repo.session.commit()
            await self.external_task_repo.session.refresh(task)

            return ExternalTaskResponse(
                id=task.id,
                external_id=task.external_id,
                external_system_id=task.external_system_id,
                title=task.title,
                description=task.description,
                status=task.status,
                url=task.url,
                external_created_at=task.external_created_at,
                external_updated_at=task.external_updated_at,
                completed_at=task.completed_at,
                last_sync=task.last_sync,
                user_id=user_id,
            )
        except Exception as e:
            if isinstance(e, (NotFoundError,)):
                raise
            raise InternalServerError(f"Failed to create task: {str(e)}", {"error": str(e)})

    async def update_external(
        self, task_id: int, data: ExternalTaskUpdateRequest, user_id: int
    ) -> ExternalTaskResponse:
        """Update an external task."""
        try:
            task = await self.external_task_repo.get_task(system_id=task_id, user_id=user_id)
        except Exception as e:
            raise InternalServerError(f"Failed to get task: {str(e)}", {"task_id": task_id})

        try:
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

            return ExternalTaskResponse(
                id=task.id,
                external_id=task.external_id,
                external_system_id=task.external_system_id,
                title=task.title,
                description=task.description,
                status=task.status,
                url=task.url,
                external_created_at=task.external_created_at,
                external_updated_at=task.external_updated_at,
                completed_at=task.completed_at,
                last_sync=task.last_sync,
                user_id=user_id,
            )
        except Exception as e:
            raise InternalServerError(
                f"Failed to update task: {str(e)}", {"task_id": task_id, "error": str(e)}
            )

    async def delete_external(self, task_id: int, user_id: int) -> None:
        """Delete an external task."""
        try:
            task = await self.external_task_repo.get_task(system_id=task_id, user_id=user_id)
        except Exception as e:
            raise InternalServerError(f"Failed to get task: {str(e)}", {"task_id": task_id})

        try:
            await self.external_task_repo.session.delete(task)
            await self.external_task_repo.session.commit()
        except Exception as e:
            raise InternalServerError(
                f"Failed to delete task: {str(e)}", {"task_id": task_id, "error": str(e)}
            )

    async def get_types(self, user_id: int) -> list[TaskTypeResponse]:
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

    async def create_type(self, user_id: int, data: TaskTypeRequest) -> TaskTypeResponse:
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

    async def update_type(
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

    async def delete_type(self, task_type_id: int, user_id: int) -> None:
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
