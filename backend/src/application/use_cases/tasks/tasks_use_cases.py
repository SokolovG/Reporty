from backend.src.application.dto.records import ExternalTaskCreateData, ExternalTaskUpdateData
from backend.src.domain.entities.external_task import ExternalTask
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.repositories import (
    ExternalSystemRepository,
    ExternalTaskRepository,
    UserRepository,
)
from backend.src.infrastructure.exceptions.api_exceptions import (
    ConflictError,
    InternalServerError,
    NotFoundError,
)


class TasksUseCase:
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

    async def create_external(self, data: ExternalTaskCreateData, user_id: int) -> ExternalTask:
        """Create a new external task."""
        try:
            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                raise NotFoundError("User", user_id)

            external_system_id = user.external_system_id
            if external_system_id is None:
                raise ConflictError(
                    "User cannot create external task - user does not have external system configured."
                )

            system = await self.external_system_repo.get_by_id(external_system_id)
            if not system:
                raise NotFoundError("ExternalSystem", external_system_id)

            task = await self.external_task_repo.create_task(
                data,
                user_id,
                external_system_id,
            )
            return task

        except NotFoundError:
            raise
        except Exception as e:
            if isinstance(e, (ConflictError, NotFoundError)):
                raise e
            raise InternalServerError(
                f"Failed to create external task: {str(e)}", {"error": str(e)}
            )

    async def update_external(
        self, task_id: int, data: ExternalTaskUpdateData, user_id: int
    ) -> ExternalTask:
        """Update an external task."""
        try:
            task = await self.external_task_repo.get_by_id(task_id, user_id)
            if not task:
                raise NotFoundError("ExternalTask", task_id)

            task.update_info(
                title=data.title,
                description=data.description,
                status=data.status,
                url=data.url,
                external_id=data.external_id,
            )

            updated_task = await self.external_task_repo.update_task(task)
            return updated_task

        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(
                f"Failed to update external task: {str(e)}", {"task_id": task_id, "error": str(e)}
            )

    async def delete_external(self, task_id: int, user_id: int) -> None:
        """Delete an external task."""
        try:
            task = await self.external_task_repo.get_by_id(task_id, user_id)
            if not task:
                raise NotFoundError("ExternalTask", task_id)

            await self.external_task_repo.delete_task(task_id, user_id)

        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(
                f"Failed to delete external task: {str(e)}", {"task_id": task_id, "error": str(e)}
            )
