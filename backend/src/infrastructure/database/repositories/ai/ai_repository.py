from advanced_alchemy import repository
from sqlalchemy import select

from backend.src.infrastructure.database.models import AIModel, AIProvider, AIProviderKey


class AIProviderRepository(repository.SQLAlchemyAsyncRepository[AIProvider]):  # type: ignore[misc]
    model_type: type[AIProvider] = AIProvider


class AIModelRepository(repository.SQLAlchemyAsyncRepository[AIModel]):  # type: ignore[misc]
    model_type: type[AIModel] = AIModel


class AIProviderKeyRepository(repository.SQLAlchemyAsyncRepository[AIProviderKey]):  # type: ignore[misc]
    model_type: type[AIProviderKey] = AIProviderKey

    async def get_all_keys_for_user(self, user_id: int) -> set[int]:
        result = await self.session.execute(
            select(AIProviderKey.ai_provider_id).where(AIProviderKey.user_id == user_id)
        )
        return set(result.scalars().all())

    async def get_user_provider_key(self, user_id: int, provider_id: int) -> AIProviderKey | None:
        """Get API key for specific user and provider."""
        result = await self.session.execute(
            select(AIProviderKey)
            .where(AIProviderKey.user_id == user_id)
            .where(AIProviderKey.ai_provider_id == provider_id)
            .where(AIProviderKey.is_active == True)  # noqa: E712
        )
        return result.scalar_one_or_none()

    async def get_key_for_user_and_provider(
        self, user_id: int, provider_id: int
    ) -> AIProviderKey | None:
        """Get API key for specific user and provider (alias for compatibility)."""
        return await self.get_user_provider_key(user_id=user_id, provider_id=provider_id)
