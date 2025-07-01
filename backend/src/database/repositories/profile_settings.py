from sqlalchemy import select

from backend.src.database.models import UserSettings, Profile
from advanced_alchemy import repository


class UserSettingsRepository(repository.SQLAlchemyAsyncRepository[UserSettings]):  # type: ignore
    """Repository for managing user settings."""

    model_type: type[UserSettings] = UserSettings

    async def get_by_user_id(self, user_id: int) -> UserSettings:
        result = await self.session.execute(
            select(UserSettings).where(UserSettings.user_id == user_id)
        )
        settings = result.scalar_one_or_none()
        if settings is None:
            # Создаем дефолтные настройки для нового пользователя
            settings = UserSettings(user_id=user_id)
            return await self.add(settings)
        return settings


class ProfileRepository(repository.SQLAlchemyAsyncRepository[Profile]):  # type: ignore
    """Repository for managing user settings."""

    model_type: type[Profile] = Profile
