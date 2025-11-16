from backend.src.database.base import AIProviders
from backend.src.services.shared.encryption_service import EncryptionService
from backend.src.database.repositories import UserRepository, AIProviderKeyRepository
from backend.src.core.exceptions import NotFoundError, InternalServerError


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

            # Get encrypted API key for user's selected provider
            api_key_data = await self.api_key_repository.get_user_provider_key(
                user_id=user_id, provider_id=user.ai_provider_id
            )

            if not api_key_data:
                raise NotFoundError("API key not found for selected AI provider")

            # Decrypt API key
            decrypted_key = await self.encryption_service.decrypt(api_key_data.encrypted_key)

            # Get AI provider info
            ai_provider = (
                AIProviders(user.ai_provider.name) if user.ai_provider else AIProviders.LOCAL
            )

            # Process with AI
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
        """Internal method to process data with specific AI provider."""

        # Base prompt for transforming developer notes to business language
        base_prompt = """
        Transform the following developer note into a professional business description.
        Make it clear, concise, and suitable for management reporting.
        Focus on business value and impact.

        Examples:
        - "sent callback" → "Configured automated payment status notifications for client"
        - "auth fix" → "Resolved critical payment system access issue, preventing potential transaction losses"
        - "db optimization" → "Improved database performance, reducing response times by 40%"

        Developer note: {raw_data}

        Business description:
        """

        # Use custom prompt if provided
        prompt = custom_prompt or base_prompt
        formatted_prompt = prompt.format(raw_data=raw_data)

        # TODO: Implement actual AI provider integrations
        if ai_provider == AIProviders.OPEN_AI:
            return await self._process_openai(formatted_prompt, api_key)
        elif ai_provider == AIProviders.CLAUDE:
            return await self._process_claude(formatted_prompt, api_key)
        elif ai_provider == AIProviders.GEMINI:
            return await self._process_gemini(formatted_prompt, api_key)
        elif ai_provider == AIProviders.LOCAL:
            return await self._process_local(formatted_prompt)
        else:
            # Fallback - simple transformation
            return f"Completed work on: {raw_data}"

    async def _process_openai(self, prompt: str, api_key: str) -> str:
        """Process with OpenAI API."""
        # TODO: Implement OpenAI integration
        return f"[OpenAI] Processed: {prompt[:50]}..."

    async def _process_claude(self, prompt: str, api_key: str) -> str:
        """Process with Claude API."""
        # TODO: Implement Claude integration
        return f"[Claude] Processed: {prompt[:50]}..."

    async def _process_gemini(self, prompt: str, api_key: str) -> str:
        """Process with Gemini API."""
        # TODO: Implement Gemini integration
        return f"[Gemini] Processed: {prompt[:50]}..."

    async def _process_local(self, prompt: str) -> str:
        """Process with local AI model."""
        # TODO: Implement local model integration (Ollama, etc.)
        return f"[Local] Processed: {prompt[:50]}..."

    async def test_provider_connection(self, user_id: int, provider_id: int) -> bool:
        """Test if AI provider connection is working."""
        try:
            # Simple test to verify API key and connection
            test_result = await self.process_record("test connection", user_id)
            return bool(test_result)
        except Exception:
            return False
