import msgspec
from litestar.dto import DTOConfig

from backend.src.api.dto.base import BaseMsgspecDTO


class TaskTypeRequest(msgspec.Struct):
    title: str
    color: str | None = None


class TaskTypeUpdateRequest(msgspec.Struct):
    id: int
    title: str | None = None
    color: str | None = None
    is_active: bool | None = None


class TaskTypeResponse(msgspec.Struct):
    id: int
    title: str
    is_active: bool
    color: str | None = None


class TaskTypeRequestDTO(BaseMsgspecDTO[TaskTypeRequest]):
    pass


class TaskTypeUpdateRequestDTO(BaseMsgspecDTO[TaskTypeUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")


class AIPreferencesUpdateRequest(msgspec.Struct):
    ai_auto_process: bool | None = None
    ai_provider_id: int | None = None


class AIPreferencesResponse(msgspec.Struct):
    ai_auto_process: bool
    ai_provider_id: int | None = None


class AIModelResponse(msgspec.Struct):
    """Response for AI model."""

    id: int
    name: str


class AIProviderResponse(msgspec.Struct):
    id: int
    name: str
    requires_api_key: bool
    is_active: bool
    models: list[AIModelResponse] = []


class AISettingsUpdateResponse(msgspec.Struct):
    ai_auto_process: bool
    ai_provider_id: int


class AIPreferencesUpdateRequestDTO(BaseMsgspecDTO[AIPreferencesUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")


class ExternalSystemResponse(msgspec.Struct):
    id: int
    name: str
    display_name: str
    api_config: dict
    is_active: bool


class AIProviderUpdateRequest(msgspec.Struct):
    api_key: str | None = None
    ai_model_id: int | None = None


class AIProviderUpdateRequestDTO(BaseMsgspecDTO[AIProviderUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")


class ExternalSystemUpdateRequest(msgspec.Struct):
    name: str | None = None
    display_name: str | None = None
    api_config: dict | None = None
    is_active: bool | None = None


class ExternalSystemUpdateRequestDTO(BaseMsgspecDTO[ExternalSystemUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")
