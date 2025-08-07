from advanced_alchemy import repository

from backend.src.database.models import User


class UserRepository(repository.SQLAlchemyAsyncRepository[User]):  # type: ignore
    model_type: type[User] = User

    async def create_user(self, email: str, name: str, password_hash: str) -> User:
        user = User(
            email=email,
            password_hash=password_hash,
            name=name,
        )
        await self.add(user)
        await self.session.commit()
        return user
