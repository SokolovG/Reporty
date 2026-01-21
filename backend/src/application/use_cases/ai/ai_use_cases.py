from backend.src.infrastructure.database.base import AIProviders
from backend.src.infrastructure.database.repositories import AIProviderKeyRepository, UserRepository
from backend.src.infrastructure.encryption.encryption_service import EncryptionService
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError, NotFoundError


class AIService:
    """Service for working with AI API."""

    def __init__(
        self,
        encryption_service: EncryptionService,
        user_repository: UserRepository,
        api_key_repository: AIProviderKeyRepository,
    ) -> None:
        self.encryption_service = encryption_service
        self.user_repository = user_repository
        self.api_key_repository = api_key_repository

    async def process_record(self, raw_data: str, user_id: int) -> str:
        """Process raw developer input into business-friendly description."""
        try:
            user = await self.user_repository.get_one(id=user_id)
            if not user.ai_provider_id:
                raise NotFoundError("AI provider not configured for user")

            api_key_data = await self.api_key_repository.get_user_provider_key(
                user_id=user_id, provider_id=user.ai_provider_id
            )

            if not api_key_data:
                raise NotFoundError("API key not found for selected AI provider")

            decrypted_key = await self.encryption_service.decrypt(api_key_data.encrypted_key)

            ai_provider = (
                AIProviders(user.ai_provider.name) if user.ai_provider else AIProviders.LOCAL
            )

            processed_string = await self._process_with_ai(
                raw_data=raw_data,
                api_key=decrypted_key,
                ai_provider=ai_provider,
                custom_prompt=user.custom_prompt,
            )

            return processed_string

        except Exception as e:
            raise InternalServerError(f"Failed to process with AI: {str(e)}")

    async def _process_with_ai(
        self,
        raw_data: str,
        api_key: str,
        ai_provider: AIProviders,
        custom_prompt: str | None = None,
    ) -> str:
        return ""
