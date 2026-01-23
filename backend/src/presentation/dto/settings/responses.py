import msgspec


class TaskTypeResponse(msgspec.Struct):
    id: int
    title: str
    is_active: bool
    color: str | None = None


class AISettingsUpdateResponse(msgspec.Struct):
    ai_auto_process: bool
    ai_provider_id: int


class ExternalSystemResponse(msgspec.Struct):
    id: int
    name: str
    display_name: str
    api_config: dict
    is_active: bool


class ExternalTaskResponse(msgspec.Struct): ...  # TODO


class AIModelResponse(msgspec.Struct):
    id: int
    name: str


class AIProviderResponse(msgspec.Struct):
    id: int
    name: str
    requires_api_key: bool
    is_active: bool
    is_key_set: bool
    models: list[AIModelResponse] = []


class AIPreferencesResponse(msgspec.Struct):
    ai_auto_process: bool
    ai_provider_id: int | None = None
