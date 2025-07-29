from dishka.integrations.litestar import inject
from litestar import Controller, post, Request

from backend.src.api.dto.user_dto import UserReadSchema, UserReadDTO


class UserController(Controller):
    @post("/me", return_dto=UserReadDTO)
    @inject
    async def get_me(self, request: Request) -> UserReadSchema:
        current_user = request.user
        user_dto = UserReadSchema(
            user_id=current_user.id,
            email=current_user.id,
            is_verified=current_user.is_verified,
            is_active=current_user.is_active,
        )
        return user_dto
