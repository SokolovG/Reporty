from advanced_alchemy import repository
from sqlalchemy import select

from backend.src.application.dto.settings import ExternalSystemUpdateData
from backend.src.domain.entities.external_system import ExternalSystem
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.models import ExternalSystemModel


class ExternalSystemRepository(
    repository.SQLAlchemyAsyncRepository[ExternalSystemModel]  # ty:ignore[invalid-type-arguments]
):
    model_type: type[ExternalSystemModel] = ExternalSystemModel

    def __init__(self, converter: Converter, **kwargs) -> None:
        super().__init__(**kwargs)
        self.converter = converter

    async def get_many(self) -> list[ExternalSystem]:
        """Get all external systems."""
        result = await self.list()
        return self.converter.convert_list(result, ExternalSystem)

    async def get_by_id(self, system_id: int) -> ExternalSystem | None:
        system = await self.get_one_or_none(id=system_id)
        if not system:
            return None

        return self.converter.convert(system, ExternalSystem)

    async def get_many_active(self) -> list[ExternalSystem]:
        result = await self.session.execute(
            select(ExternalSystemModel).where(ExternalSystemModel.is_active)
        )
        systems = result.scalars().all()
        return self.converter.convert_list(list(systems), ExternalSystem)

    async def update_system(self, system_id: int, data: ExternalSystemUpdateData) -> ExternalSystem:
        """Update an external system."""
        system = await self.get(system_id)

        if data.name is not None:
            system.name = data.name
        if data.display_name is not None:
            system.display_name = data.display_name
        if data.api_config is not None:
            system.api_config = data.api_config
        if data.is_active is not None:
            system.is_active = data.is_active

        await self.session.commit()
        await self.session.refresh(system)
        return self.converter.convert(system, ExternalSystem)
