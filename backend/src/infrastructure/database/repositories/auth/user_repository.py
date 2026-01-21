from advanced_alchemy import repository

from backend.src.infrastructure.database.models import UserModel


class UserRepository(repository.SQLAlchemyAsyncRepository[UserModel]):  # ty: ignore  # noqa: F821
    model_type: type[UserModel] = UserModel

    async def create_user(
        self,
        email: str,
        name: str,
        password_hash: str,
        display_name: str | None = None,
        department: str | None = None,
        position: str | None = None,
        ai_auto_process: bool = False,
        is_admin: bool = False,
    ) -> UserModel:
        """Create a new user with profile information."""
        user = UserModel(
            email=email,
            password_hash=password_hash,
            name=name,
            display_name=display_name,
            department=department,
            position=position,
            ai_auto_process=ai_auto_process,
            is_admin=is_admin,
        )
        await self.add(user)
        await self.session.commit()
        return user

    async def update_profile(
        self,
        user_id: int,
        display_name: str | None = None,
        department: str | None = None,
        position: str | None = None,
        email: str | None = None,
    ) -> UserModel:
        """Update user profile information."""
        user = await self.get_one(id=user_id)

        if display_name is not None:
            user.display_name = display_name
        if department is not None:
            user.department = department
        if position is not None:
            user.position = position
        if email is not None:
            user.email = email

        await self.session.commit()
        return user
