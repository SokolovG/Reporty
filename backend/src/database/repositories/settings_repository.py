from collections.abc import Sequence

from sqlalchemy import select
from advanced_alchemy import repository

from backend.src.database.models import TaskType, AIProvider, UserProfile, ExternalSystem


class AIProviderRepository(repository.SQLAlchemyAsyncRepository[AIProvider]):  # type: ignore
    model_type: type[AIProvider] = AIProvider


class UserProfileRepository(repository.SQLAlchemyAsyncRepository[UserProfile]):  # type: ignore
    """Repository for managing user profiles and settings"""

    model_type: type[UserProfile] = UserProfile

    async def get_by_user_id(self, user_id: int) -> UserProfile:
        result = await self.session.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()

        if profile is None:
            profile = UserProfile(user_id=user_id)
            profile = await self.add(profile)
            await self.session.commit()

        return profile

    async def get_task_types_by_user_id(self, user_id: int) -> Sequence[TaskType]:
        """Get task types for user."""
        result = await self.session.execute(
            select(TaskType)
            .join(UserProfile, TaskType.user_profile_id == UserProfile.id)
            .where(UserProfile.user_id == user_id)
            .where(TaskType.is_active == True)  # noqa: E712
            .order_by(TaskType.title)
        )
        return result.scalars().all()

    async def create_task_type(
        self, user_id: int, title: str, color: str | None = None
    ) -> TaskType:
        """Create new task type for user."""
        profile = await self.get_by_user_id(user_id)

        task_type = TaskType(user_profile_id=profile.id, title=title, color=color)

        self.session.add(task_type)
        await self.session.commit()
        await self.session.refresh(task_type)
        return task_type


class ExternalSystemRepository(repository.SQLAlchemyAsyncRepository[ExternalSystem]):  # type: ignore
    model_type: type[ExternalSystem] = ExternalSystem
