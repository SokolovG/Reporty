from advanced_alchemy import repository
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.src.domain.entities.ai import AIProvider, AIProviderKey
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.models import AIModel, AIProviderKeyModel, AIProviderModel


class AIProviderRepository(repository.SQLAlchemyAsyncRepository[AIProviderModel]):  # type: ignore[misc]
    model_type: type[AIProviderModel] = AIProviderModel

    def __init__(self, converter: Converter, **kwargs) -> None:
        super().__init__(**kwargs)
        self.converter = converter

    async def get_active_providers_with_models(self) -> list[AIProvider]:
        """Get all active AI providers with their models loaded."""

        result = await self.session.execute(
            select(AIProviderModel)
            .where(AIProviderModel.is_active == True)  # noqa: E712
            .options(selectinload(AIProviderModel.models))
        )
        models = list(result.scalars().all())
        return self.converter.convert_list(models, AIProvider)

    async def get_many_active(self) -> list[AIProvider]:
        """Get all active providers."""
        result = await self.session.execute(
            select(AIProviderModel)
            .where(AIProviderModel.is_active == True)  # noqa: E712
            .options(selectinload(AIProviderModel.models))
        )
        models = list(result.scalars().all())
        return self.converter.convert_list(models, AIProvider)

    async def get_by_id_with_models(self, provider_id: int) -> AIProvider | None:
        """Get AI provider by ID with models loaded."""

        result = await self.session.execute(
            select(AIProviderModel)
            .where(AIProviderModel.id == provider_id)
            .options(selectinload(AIProviderModel.models))
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self.converter.convert(model, AIProvider)


class AIModelRepository(repository.SQLAlchemyAsyncRepository[AIModel]):  # type: ignore[misc]
    model_type: type[AIModel] = AIModel


class AIProviderKeyRepository(repository.SQLAlchemyAsyncRepository[AIProviderKeyModel]):  # type: ignore[misc]
    model_type: type[AIProviderKeyModel] = AIProviderKeyModel

    def __init__(self, converter: Converter, **kwargs) -> None:
        super().__init__(**kwargs)
        self.converter = converter

    async def get_all_keys_for_user(self, user_id: int) -> set[int]:
        result = await self.session.execute(
            select(AIProviderKeyModel.ai_provider_id).where(AIProviderKeyModel.user_id == user_id)
        )
        return set(result.scalars().all())

    async def get_user_provider_key(self, user_id: int, provider_id: int) -> AIProviderKey | None:
        """Get API key for specific user and provider."""
        result = await self.session.execute(
            select(AIProviderKeyModel)
            .where(AIProviderKeyModel.user_id == user_id)
            .where(AIProviderKeyModel.ai_provider_id == provider_id)
            .where(AIProviderKeyModel.is_active == True)  # noqa: E712
        )
        key = result.scalar_one_or_none()
        if key is None:
            return None
        return self.converter.convert(key, AIProviderKey)
