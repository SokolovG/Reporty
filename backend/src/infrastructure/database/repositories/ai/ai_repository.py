from advanced_alchemy import repository
from sqlalchemy import select

from backend.src.infrastructure.database.models import AIModel, AIProviderKeyModel, AIProviderModel


class AIProviderRepository(repository.SQLAlchemyAsyncRepository[AIProviderModel]):  # type: ignore[misc]
    model_type: type[AIProviderModel] = AIProviderModel


class AIModelRepository(repository.SQLAlchemyAsyncRepository[AIModel]):  # type: ignore[misc]
    model_type: type[AIModel] = AIModel


class AIProviderKeyRepository(repository.SQLAlchemyAsyncRepository[AIProviderKeyModel]):  # type: ignore[misc]
    model_type: type[AIProviderKeyModel] = AIProviderKeyModel

    async def get_all_keys_for_user(self, user_id: int) -> set[int]:
        result = await self.session.execute(
            select(AIProviderKeyModel.ai_provider_id).where(AIProviderKeyModel.user_id == user_id)
        )
        return set(result.scalars().all())

    async def get_active_providers(self) -> list[AIProviderModel]:
        result = await self.session.execute(
            select(AIProviderModel).where(AIProviderModel.is_active)
        )
        return result.scalars().all()

    async def get_user_provider_key(
        self, user_id: int, provider_id: int
    ) -> AIProviderKeyModel | None:
        """Get API key for specific user and provider."""
        result = await self.session.execute(
            select(AIProviderKeyModel)
            .where(AIProviderKeyModel.user_id == user_id)
            .where(AIProviderKeyModel.ai_provider_id == provider_id)
            .where(AIProviderKeyModel.is_active == True)  # noqa: E712
        )
        return result.scalar_one_or_none()

    async def get_key_for_user_and_provider(
        self, user_id: int, provider_id: int
    ) -> AIProviderKeyModel | None:
        """Get API key for specific user and provider (alias for compatibility)."""
        return await self.get_user_provider_key(user_id=user_id, provider_id=provider_id)
