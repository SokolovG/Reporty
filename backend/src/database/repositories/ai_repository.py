from advanced_alchemy import repository

from backend.src.database.models import AIModel, AIProvider


class AIProviderRepository(repository.SQLAlchemyAsyncRepository[AIProvider]):  # type: ignore
    model_type: type[AIProvider] = AIProvider


class AIModelRepository(repository.SQLAlchemyAsyncRepository[AIModel]):  # type: ignore
    model_type: type[AIModel] = AIModel
