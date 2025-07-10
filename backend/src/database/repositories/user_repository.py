from advanced_alchemy import repository
from backend.src.database.models import User


class UserRepository(repository.SQLAlchemyAsyncRepository[User]):  # type: ignore
    model_type: type[User] = User
