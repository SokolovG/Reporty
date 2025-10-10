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


class TaskTypeResponseDTO(BaseMsgspecDTO[TaskTypeResponse]):
    pass

class AISettingsUpdateRequest(msgspec.Struct):
    auto_ai_enable: bool
    ai_provider: str


class AIProviderResponse(msgspec.Struct):
    id: int
    name: str
    requires_api_key: bool
    is_active: bool
    base_prompt: str | None = None
    model_name: str | None = None

class AISettingsUpdateResponse(msgspec.Struct):
    auto_ai_enable: bool
    ai_provider: str

class AIProviderResponseDTO(BaseMsgspecDTO[AIProviderResponse]):
    pass

class AISettingsUpdateResponseDTO(BaseMsgspecDTO[AISettingsUpdateResponse]):
    pass

class ExternalSystemResponse(msgspec.Struct):
    id: int
    name: str
    display_name: str
    api_config: dict
    is_active: bool


class ExternalSystemResponseDTO(BaseMsgspecDTO[ExternalSystemResponse]):
    pass


class AIProviderUpdateRequest(msgspec.Struct):
    base_prompt: str | None = None
    model_name: str | None = None
    requires_api_key: bool | None = None
    is_active: bool | None = None


class AIProviderUpdateRequestDTO(BaseMsgspecDTO[AIProviderUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")

class AISettingsUpdateRequestDTO(BaseMsgspecDTO[AISettingsUpdateRequest]):
    pass
    

class ExternalSystemUpdateRequest(msgspec.Struct):
    name: str | None = None
    display_name: str | None = None
    api_config: dict | None = None
    is_active: bool | None = None


class ExternalSystemUpdateRequestDTO(BaseMsgspecDTO[ExternalSystemUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")
