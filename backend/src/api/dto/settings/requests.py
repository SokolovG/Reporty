import msgspec


class TaskTypeRequest(msgspec.Struct):
    title: str
    color: str | None = None


class TaskTypeUpdateRequest(msgspec.Struct):
    id: int
    title: str | None = None
    color: str | None = None
    is_active: bool | None = None


class AIPreferencesUpdateRequest(msgspec.Struct):
    ai_auto_process: bool | None = None
    ai_provider_id: int | None = None
    custom_prompt: str | None = None


class AIProviderUpdateRequest(msgspec.Struct):
    api_key: str | None = None
    ai_model_id: int | None = None


class ExternalSystemUpdateRequest(msgspec.Struct):
    name: str | None = None
    display_name: str | None = None
    api_config: dict | None = None
    is_active: bool | None = None
