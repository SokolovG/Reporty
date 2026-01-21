from backend.src.domain.entities.user import User
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.repositories import UserRepository
from backend.src.infrastructure.exceptions.api_exceptions import NotFoundError


class UserProfileUseCases:
    """Use cases for user-related operations."""

    def __init__(self, user_repository: UserRepository, converter: Converter) -> None:
        self.user_repository = user_repository
        self.converter = converter

    async def get_profile(self, user_id: int) -> User:
        """Get user profile by ID."""
        user_model = await self.user_repository.get_one_or_none(id=user_id)
        if not user_model:
            raise NotFoundError("User", user_id)

        domain_user = self.converter.convert(user_model, User)
        return domain_user

    async def update_profile(self, user_id: int, converter: Converter, **kwargs) -> User:
        """Update user profile."""
        user_model = await self.user_repository.get_one_or_none(id=user_id)
        if not user_model:
            raise NotFoundError("User", user_id)

        domain_user = converter.convert(user_model, User)

        # TODO: Implement profile update logic
        return domain_user
