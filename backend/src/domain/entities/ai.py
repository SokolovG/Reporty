from dataclasses import dataclass, field


@dataclass
class AIModel:
    """Domain entity representing an AI model."""

    id: int
    name: str
    ai_provider_id: int


@dataclass
class AIProvider:
    """Domain entity representing an AI provider."""

    id: int
    name: str
    requires_api_key: bool
    is_active: bool
    base_prompt: str | None = None
    models: list[AIModel] = field(default_factory=list)

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False


@dataclass
class AIProviderKey:
    """Domain entity representing encrypted API key."""

    id: int
    user_id: int
    ai_provider_id: int
    encrypted_key: bytes
    is_active: bool = True
