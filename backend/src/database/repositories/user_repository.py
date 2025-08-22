from advanced_alchemy import repository

from backend.src.database.models import User


class UserRepository(repository.SQLAlchemyAsyncRepository[User]):  # type: ignore
    model_type: type[User] = User

    async def create_user(self, email: str, name: str, password_hash: str) -> User:
        """Create a new user."""
        user = User(
            email=email,
            password_hash=password_hash,
            name=name,
        )
        await self.add(user)
        await self.session.commit()
        return user

    async def get_hashed_password(self, email: str) -> str:
        """Get user's password hash by email."""
        user = await self.get_one(email=email)
        hash: str = user.password_hash
        return hash
