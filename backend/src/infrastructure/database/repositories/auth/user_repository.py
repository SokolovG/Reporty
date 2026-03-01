from advanced_alchemy import repository

from backend.src.application.dto.auth import RegisterData
from backend.src.domain.entities.user import User
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.models import UserModel


class UserRepository(repository.SQLAlchemyAsyncRepository[UserModel]):  # ty: ignore  # noqa: F821
    model_type: type[UserModel] = UserModel

    def __init__(self, converter: Converter, **kwargs) -> None:
        super().__init__(**kwargs)
        self.converter = converter

    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email."""
        user_model = await self.get_one_or_none(email=email)
        if user_model is None:
            return None

        return self.converter.convert(user_model, User)

    async def get_user_by_id(self, id: int) -> User | None:
        """Get user by id."""
        user_model = await self.get_one_or_none(id=id)
        if user_model is None:
            return None

        return self.converter.convert(user_model, User)

    async def create_user(
        self,
        data: RegisterData,
        hashed_password: str,
    ) -> User:
        """Create a new user with profile information."""
        user_model = UserModel(
            email=data.email,
            password_hash=hashed_password,
            name=data.name,
            display_name=data.display_name,
            department=data.department,
            position=data.position,
            ai_auto_process=data.ai_auto_process,
        )
        await self.add(user_model)
        await self.session.commit()
        return self.converter.convert(user_model, User)

    async def update_user(self, user: User) -> User:
        """Update existing user."""
        user_model = await self.get(user.id)

        user_model.password_hash = user.password_hash
        user_model.is_active = user.is_active
        user_model.is_admin = user.is_admin
        user_model.display_name = user.display_name
        user_model.department = user.department
        user_model.position = user.position
        user_model.email = user.email
        user_model.name = user.name
        user_model.ai_auto_process = user.ai_auto_process
        user_model.is_verify = user.is_verify
        user_model.ai_provider_id = user.ai_provider_id
        user_model.ai_model_id = user.ai_model_id
        user_model.custom_prompt = user.custom_prompt

        await self.session.commit()
        await self.session.refresh(user_model)
        return self.converter.convert(user_model, User)
