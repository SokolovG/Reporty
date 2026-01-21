from backend.src.infrastructure.database.repositories import UserRepository
from backend.src.infrastructure.exceptions.api_exceptions import NotFoundError
from backend.src.presentation.dto.auth.responses import UserResponse
from backend.src.presentation.dto.converters import user_to_response


class UserUseCases:
    """Use cases for user-related operations."""

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def get_user_profile(self, user_id: int) -> UserResponse:
        """Get user profile by ID."""
        user = await self.user_repository.get_one_or_none(id=user_id)
        if not user:
            raise NotFoundError("User", user_id)

        return user_to_response(user)

    async def update_user_profile(self, user_id: int, **kwargs) -> UserResponse:
        """Update user profile."""
        user = await self.user_repository.get_one_or_none(id=user_id)
        if not user:
            raise NotFoundError("User", user_id)

        # TODO: Implement profile update logic
        return user_to_response(user)
