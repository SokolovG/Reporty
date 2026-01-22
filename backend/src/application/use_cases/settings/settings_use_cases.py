from sqlalchemy import select

from backend.src.application.dto.settings import ExternalSystemUpdateData
from backend.src.domain.entities.external_system import ExternalSystem
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.models import ExternalSystemModel
from backend.src.infrastructure.database.repositories import (
    AIModelRepository,
    AIProviderRepository,
    ExternalSystemRepository,
    UserRepository,
)
from backend.src.infrastructure.database.repositories.ai.ai_repository import (
    AIProviderKeyRepository,
)
from backend.src.infrastructure.encryption.encryption_service import EncryptionService
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError


class SettingsUseCases:
    """Service for managing user settings and preferences."""

    def __init__(
        self,
        ai_provider_repository: AIProviderRepository,
        ai_models_repository: AIModelRepository,
        user_repository: UserRepository,
        external_system_repository: ExternalSystemRepository,
        encryption_service: EncryptionService,
        api_key_repo: AIProviderKeyRepository,
        converter: Converter,
    ) -> None:
        self.encryption_service = encryption_service
        self.ai_provider_repository = ai_provider_repository
        self.ai_models_repository = ai_models_repository
        self.user_repository = user_repository
        self.external_system_repository = external_system_repository
        self.api_key_repo = api_key_repo
        self.converter = converter

    # External Systems Management
    async def get_external_systems(self) -> list[ExternalSystem]:
        """Get all external systems."""
        try:
            result = await self.external_system_repository.session.execute(
                select(ExternalSystemModel)
            )
            domain_systems: list[ExternalSystem] = []
            for system_model in result.scalars().all():
                domain_systems.append(self.converter.convert(system_model, ExternalSystem))

            return domain_systems

        except Exception as e:
            raise InternalServerError(f"Failed to get external systems: {str(e)}")

    async def get_active_external_systems(self) -> list[ExternalSystem]:
        """Get only active external systems."""
        try:
            result = await self.external_system_repository.session.execute(
                select(ExternalSystemModel).where(ExternalSystemModel.is_active == True)  # noqa: E712
            )

            domain_systems: list[ExternalSystem] = []
            for system_model in result.scalars().all():
                domain_systems.append(self.converter.convert(system_model, ExternalSystem))

            return domain_systems

        except Exception as e:
            raise InternalServerError(f"Failed to get active external systems: {str(e)}")

    async def update_external_system(
        self, system_id: int, data: ExternalSystemUpdateData
    ) -> ExternalSystem:
        """Update an external system."""
        try:
            system = await self.external_system_repository.get(system_id)

            if data.name is not None:
                system.name = data.name
            if data.display_name is not None:
                system.display_name = data.display_name
            if data.api_config is not None:
                system.api_config = data.api_config
            if data.is_active is not None:
                system.is_active = data.is_active

            updated_system_model = await self.external_system_repository.update(system)
            await self.external_system_repository.session.commit()
            domain_updated_system = self.converter.convert(updated_system_model, ExternalSystem)
            return domain_updated_system

        except Exception as e:
            raise InternalServerError(
                f"Failed to update external system: {str(e)}", {"system_id": system_id}
            )
