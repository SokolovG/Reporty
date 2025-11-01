from advanced_alchemy import repository
from sqlalchemy import select

from backend.src.database.models import AIModel, AIProvider, AIProviderKey


class AIProviderRepository(repository.SQLAlchemyAsyncRepository[AIProvider]):  # type: ignore
    model_type: type[AIProvider] = AIProvider


class AIModelRepository(repository.SQLAlchemyAsyncRepository[AIModel]):  # type: ignore
    model_type: type[AIModel] = AIModel


class AIProviderKeyRepository(repository.SQLAlchemyAsyncRepository[AIProviderKey]):  # type: ignore
    model_type: type[AIProviderKey] = AIProviderKey

    async def get_all_keys_for_user(self, user_id: int) -> set[int]:
        result = await self.session.execute(
            select(AIProviderKey.ai_provider_id).where(AIProviderKey.user_id == user_id)
        )
        return set(result.scalars().all())
