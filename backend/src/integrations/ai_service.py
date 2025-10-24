from backend.src.database.base import AIProviders
from backend.src.services import EncryptionService


class AIService:
    """Service for working with AI API."""

    def __init__(self, encryption_service: EncryptionService) -> None:
        self.encryption_service = encryption_service

    async def process(self, raw_data: str, user_id: int) -> str:
        # TODO: real data
        api_key = ""
        ai_provider = AIProviders.LOCAL

        processed_string = await self._process_ai(raw_data, api_key, ai_provider)
        return processed_string

    async def _process_ai(self, raw_data: str, api_key: str, ai_provider: AIProviders) -> str:
        return "fertig"
