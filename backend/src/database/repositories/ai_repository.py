from advanced_alchemy import repository

from backend.src.database.models import AIProvider


class AIProviderRepository(repository.SQLAlchemyAsyncRepository[AIProvider]):  # type: ignore
    model_type: type[AIProvider] = AIProvider
