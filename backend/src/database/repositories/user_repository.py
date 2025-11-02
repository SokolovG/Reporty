from advanced_alchemy import repository

from backend.src.database.models import User


class UserRepository(repository.SQLAlchemyAsyncRepository[User]):  # type: ignore
    model_type: type[User] = User

    async def create_user(
        self,
        email: str,
        name: str,
        password_hash: str,
        display_name: str | None = None,
        department: str | None = None,
        position: str | None = None,
        ai_auto_process: bool = False,
    ) -> User:
        """Create a new user with profile information."""
        user = User(
            email=email,
            password_hash=password_hash,
            name=name,
            display_name=display_name,
            department=department,
            position=position,
            ai_auto_process=ai_auto_process,
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
    ) -> User:
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

    # async def get_task_types_by_user_id(self, user_id: int) -> Sequence[TaskType]:
    #     """Get task types for user."""
    #     result = await self.session.execute(
    #         select(TaskType)
    #         .join(UserProfile, TaskType.user_profile_id == UserProfile.id)
    #         .where(UserProfile.user_id == user_id)
    #         .where(TaskType.is_active == True)  # noqa: E712
    #         .order_by(TaskType.title)
    #     )
    #     return result.scalars().all()

    # async def create_task_type(
    #     self, user_id: int, title: str, color: str | None = None
    # ) -> TaskType:
    #     """Create new task type for user."""
    #     profile = await self.get_by_user_id(user_id)

    #     task_type = TaskType(user_profile_id=profile.id, title=title, color=color)

    #     self.session.add(task_type)
    #     await self.session.commit()
    #     await self.session.refresh(task_type)
    #     return task_type
