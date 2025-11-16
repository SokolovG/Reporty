from backend.src.core.exceptions import InternalServerError
from backend.src.database.repositories import UserRepository
from backend.src.api.dto.auth_dto import UserResponse, UserUpdateRequest
from backend.src.api.dto.converters import user_to_response


class UserService:
    """Service for user profile management."""

    def __init__(self, user_repository: UserRepository) -> None:
        self.repo = user_repository

    async def get_user(self, user_id: int) -> UserResponse:
        """Get user with all information."""
        try:
            user = await self.repo.get_one(id=user_id)
            return user_to_response(user)
        except Exception as e:
            raise InternalServerError(f"Failed to get user: {str(e)}", {"user_id": user_id})

    async def update_user(self, user_id: int, data: UserUpdateRequest) -> UserResponse:
        """Update user information."""
        try:
            user = await self.repo.update_profile(
                user_id=user_id,
                display_name=data.display_name,
                department=data.department,
                position=data.position,
                email=data.email,
            )
            return user_to_response(user)
        except Exception as e:
            raise InternalServerError(f"Failed to update user: {str(e)}", {"user_id": user_id})
