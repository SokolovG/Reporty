from datetime import datetime, timezone

from advanced_alchemy import repository
from sqlalchemy import select

from backend.src.application.dto.records import ExternalTaskCreateData
from backend.src.domain.entities.external_system import ExternalSystem
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.models import ExternalSystemModel, ExternalTaskModel
from backend.src.infrastructure.exceptions.api_exceptions import NotFoundError


class ExternalSystemRepository(
    repository.SQLAlchemyAsyncRepository[ExternalSystemModel]  # ty:ignore[invalid-type-arguments]
):
    model_type: type[ExternalSystemModel] = ExternalSystemModel

    def __init__(self, converter: Converter, **kwargs) -> None:
        super().__init__(**kwargs)
        self.converter = converter

    async def get_external_systems(self) -> list[ExternalSystemModel]:
        """Get all external systems."""
        result = await self.list()
        return result

    async def create_external_system(
        self, data: ExternalTaskCreateData, user_id: int
    ) -> ExternalTaskModel:
        result = await self.session.execute(
            select(self.model_type).where(self.model_type.name == "manual")
        )

        system = result.scalar_one_or_none()

        if not system:
            raise NotFoundError(
                "External system 'manual'",
                details={"system_name": "manual", "help": "Create system via admin panel"},
            )

        now = datetime.now(timezone.utc)
        task = ExternalTaskModel(
            external_id=data.external_id if data.external_id is not None else None,
            external_system_id=system.id,
            title=data.title,
            status="OPEN",
            url=data.url,
            external_created_at=now,
            user_id=user_id,
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def get_active_external_systems(self) -> list[ExternalSystem]:
        result = await self.session.execute(
            select(ExternalSystemModel).where(ExternalSystemModel.is_active)
        )
        systems = result.scalars().all()
        return self.converter.convert_list(list(systems), ExternalSystem)
