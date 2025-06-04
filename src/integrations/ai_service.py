from src.core.settings import settings


class AIService:
    """Service for working with AI API."""

    def __init__(self) -> None:
        self.api_key = settings.ai_api_key
        self.model = ""
        self.max_tokens = ""
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.prompt_template = ""
