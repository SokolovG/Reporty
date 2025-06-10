from backend.src.database.base import AIProviders
from backend.src.database.repositories import UserSettingsRepository
from backend.src.services import CryptoService


class AIService:
    """Service for working with AI API."""

    def __init__(
        self, settings_repo: UserSettingsRepository, crypto_service: CryptoService
    ) -> None:
        self.settings_repo = settings_repo
        self.crypto_service = crypto_service

    async def process(self, raw_data: str, user_id: int) -> str:
        settings = await self.settings_repo.get_by_user_id(user_id)
        api_key = self.crypto_service.decrypt(settings.encrypted_api_key)
        ai_provider = settings.ai_provider

        processed_string = await self._process_ai(raw_data, api_key, ai_provider)
        return processed_string

    async def _process_ai(self, raw_data: str, api_key: str, ai_provider: AIProviders) -> str:
        return "fertig"
