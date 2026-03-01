from backend.src.application.dto.auth import UpdateUserData
from backend.src.application.ports.repositories import (
    IUserRepository,
)
from backend.src.domain.entities.user import User
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError, NotFoundError


class UserUseCases:
    """Service for managing user settings and preferences."""

    def __init__(
        self,
        user_repository: IUserRepository,
        converter: Converter,
    ) -> None:
        self.user_repository = user_repository
        self.converter = converter

    async def get(self, user_id: int) -> User:
        """Get user with all information."""
        try:
            user = await self.user_repository.get_user_by_id(id=user_id)
            if not user:
                raise NotFoundError("User", user_id)
            return user

        except Exception as e:
            raise InternalServerError(f"Failed to get user: {str(e)}", {"user_id": user_id})

    async def update(self, user_id: int, data: UpdateUserData) -> User:
        """Update user profile information."""
        try:
            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                raise NotFoundError("User", user_id)

            if (
                data.display_name is not None
                or data.department is not None
                or data.position is not None
            ):
                user.update_profile(
                    display_name=data.display_name,
                    department=data.department,
                    position=data.position,
                )

            if data.email is not None:
                user.email = data.email

            updated_user = await self.user_repository.update_user(user)
            return updated_user

        except Exception as e:
            if isinstance(e, NotFoundError):
                raise e
            raise InternalServerError(f"Failed to update user: {str(e)}", {"user_id": user_id})
