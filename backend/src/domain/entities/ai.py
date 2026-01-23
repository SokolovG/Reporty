from dataclasses import dataclass


@dataclass
class AIPreferencesData:
    ai_auto_process: bool
    ai_provider_id: int | None = None


@dataclass
class AIModelData:
    """Response for AI model."""

    id: int
    name: str


@dataclass
class AIProviderData:
    id: int
    name: str
    requires_api_key: bool
    is_active: bool
    is_key_set: bool
    models: list[AIModelData] = []


class AIProvider: ...


class AIProviderKey: ...
