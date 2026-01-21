from backend.src.infrastructure.database.repositories import UserRepository
from backend.src.infrastructure.database.repositories.ai.ai_repository import (
    AIProviderKeyRepository,
)
from backend.src.infrastructure.encryption.encryption_service import EncryptionService
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError


class AIUseCases:
    """Use cases for AI-related operations."""

    def __init__(
        self,
        encryption_service: EncryptionService,
        user_repository: UserRepository,
        api_key_repository: AIProviderKeyRepository,
    ) -> None:
        self.encryption_service = encryption_service
        self.user_repository = user_repository
        self.api_key_repository = api_key_repository

    async def process_record(
        self, raw_input: str, user_id: int
    ) -> str:  # TODO: change return type tp domain entity
        """Process record content with AI."""
        try:
            # TODO: Implement actual AI processing logic
            # This is a placeholder implementation
            processed_content = f"AI processed: {raw_input}"
            return processed_content

        except Exception as e:
            raise InternalServerError(f"Failed to process record with AI: {str(e)}")

    async def get_user_api_key(self, user_id: int, provider_id: int) -> str | None:
        """Get decrypted API key for user and provider."""
        try:
            api_key_record = await self.api_key_repository.get_key_for_user_and_provider(
                user_id=user_id, provider_id=provider_id
            )
            if not api_key_record:
                return None

            decrypted_key = await self.encryption_service.decrypt(api_key_record.encrypted_key)
            return decrypted_key
        except Exception as e:
            raise InternalServerError(f"Failed to get API key: {str(e)}")
