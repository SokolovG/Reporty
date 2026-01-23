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
