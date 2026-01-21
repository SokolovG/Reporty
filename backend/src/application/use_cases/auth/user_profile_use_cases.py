from backend.src.infrastructure.database.models import UserModel
from backend.src.infrastructure.database.repositories import UserRepository
from backend.src.infrastructure.exceptions.api_exceptions import NotFoundError


class UserProfileUseCases:
    """Use cases for user-related operations."""

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def get_profile(self, user_id: int) -> UserModel:
        """Get user profile by ID."""
        user = await self.user_repository.get_one_or_none(id=user_id)
        if not user:
            raise NotFoundError("User", user_id)

        return user

    async def update_profile(self, user_id: int, **kwargs) -> UserModel:
        """Update user profile."""
        user = await self.user_repository.get_one_or_none(id=user_id)
        if not user:
            raise NotFoundError("User", user_id)

        # TODO: Implement profile update logic
        return user
