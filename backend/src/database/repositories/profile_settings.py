from backend.src.database.models import UserSettings, Profile
from advanced_alchemy import repository


class UserSettingsRepository(repository.SQLAlchemyAsyncRepository[UserSettings]):  # type: ignore
    """Repository for managing user settings."""

    model_type: type[UserSettings] = UserSettings

    async def get_by_user_id(self, user_id: int) -> UserSettings:  # type: ignore
        pass


class ProfileRepository(repository.SQLAlchemyAsyncRepository[Profile]):  # type: ignore
    """Repository for managing user settings."""

    model_type: type[Profile] = Profile
