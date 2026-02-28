from backend.src.application.ports.repositories import IUserRepository
from backend.src.domain.entities.user import User
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError, NotFoundError


class UserProfileUseCases:
    """Use cases for user-related operations."""

    def __init__(self, user_repository: IUserRepository, converter: Converter) -> None:
        self.user_repository = user_repository
        self.converter = converter

    async def get_profile(self, user_id: int) -> User:
        """Get user profile by ID."""
        user = await self.user_repository.get_user_by_id(id=user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return user

    async def update_profile(self, user_id: int, **kwargs) -> User:
        """Update user profile information."""
        try:
            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                raise NotFoundError("User", user_id)

            user.update_profile(
                display_name=kwargs.get("display_name"),
                department=kwargs.get("department"),
                position=kwargs.get("position"),
            )

            if "ai_auto_process" in kwargs:
                user.ai_auto_process = kwargs["ai_auto_process"]

            updated_user = await self.user_repository.update_user(user)
            return updated_user

        except Exception as e:
            if isinstance(e, NotFoundError):
                raise e
            raise InternalServerError(
                f"Failed to update user profile: {str(e)}", {"user_id": user_id}
            )
