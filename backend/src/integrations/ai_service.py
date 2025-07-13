from backend.src.database.base import AIProviders
from backend.src.database.repositories import UserProfileRepository
from backend.src.services import CryptoService


class AIService:
    """Service for working with AI API."""

    def __init__(
        self, user_profile_settings: UserProfileRepository, crypto_service: CryptoService
    ) -> None:
        self.user_profile_settings = user_profile_settings
        self.crypto_service = crypto_service

    async def process(self, raw_data: str, user_id: int) -> str:
        settings = await self.user_profile_settings.get_by_user_id(user_id)
        api_key = self.crypto_service.decrypt(settings.encrypted_api_key)
        ai_provider = AIProviders[settings.ai_provider]

        processed_string = await self._process_ai(raw_data, api_key, ai_provider)
        return processed_string

    async def _process_ai(self, raw_data: str, api_key: str, ai_provider: AIProviders) -> str:
        return "fertig"
