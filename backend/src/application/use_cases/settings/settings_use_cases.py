from backend.src.application.dto.settings import ExternalSystemUpdateData
from backend.src.application.ports.repositories import (
    IAIModelRepository,
    IAIProviderKeyRepository,
    IAIProviderRepository,
    IExternalSystemRepository,
    IUserRepository,
)
from backend.src.domain.entities.external_system import ExternalSystem
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError


class SettingsUseCases:
    """Service for managing user settings and preferences."""

    def __init__(
        self,
        ai_provider_repository: IAIProviderRepository,
        ai_models_repository: IAIModelRepository,
        user_repository: IUserRepository,
        external_system_repository: IExternalSystemRepository,
        api_key_repo: IAIProviderKeyRepository,
        converter: Converter,
    ) -> None:
        self.ai_provider_repository = ai_provider_repository
        self.ai_models_repository = ai_models_repository
        self.user_repository = user_repository
        self.external_system_repository = external_system_repository
        self.api_key_repo = api_key_repo
        self.converter = converter

    async def get_external_systems(self) -> list[ExternalSystem]:
        """Get all external systems."""
        try:
            return list(await self.external_system_repository.get_many())

        except Exception as e:
            raise InternalServerError(f"Failed to get external systems: {str(e)}")

    async def get_active_external_systems(self) -> list[ExternalSystem]:
        """Get only active external systems."""
        try:
            return list(await self.external_system_repository.get_many_active())

        except Exception as e:
            raise InternalServerError(f"Failed to get active external systems: {str(e)}")

    async def update_external_system(
        self, system_id: int, data: ExternalSystemUpdateData
    ) -> ExternalSystem:
        """Update an external system."""
        try:
            return await self.external_system_repository.update_system(system_id, data)

        except Exception as e:
            raise InternalServerError(
                f"Failed to update external system: {str(e)}", {"system_id": system_id}
            )
