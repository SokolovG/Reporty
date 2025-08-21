from advanced_alchemy import repository

from backend.src.database.models import User


class UserRepository(repository.SQLAlchemyAsyncRepository[User]):
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

    async def get_hashed_password(self, email: str) -> str:
        user = await self.get_one(email=email)
        password_hash: str = user.password_hash
        return password_hash
