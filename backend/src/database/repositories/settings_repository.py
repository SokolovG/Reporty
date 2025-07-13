from sqlalchemy import select
from advanced_alchemy import repository

from backend.src.database.models import TaskType, AIProvider, UserProfile, ExternalSystem


class TaskTypeRepository(repository.SQLAlchemyAsyncRepository[TaskType]):  # type: ignore
    model_type: type[TaskType] = TaskType


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


class ExternalSystemRepository(repository.SQLAlchemyAsyncRepository[ExternalSystem]):  # type: ignore
    model_type: type[ExternalSystem] = ExternalSystem
