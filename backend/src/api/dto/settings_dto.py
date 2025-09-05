import msgspec
from litestar.dto import DTOConfig

from backend.src.api.dto.base import BaseMsgspecDTO


class TaskTypeRequest(msgspec.Struct):
    id: int
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


class AIProviderResponse(msgspec.Struct):
    id: int
    name: str
    requires_api_key: bool
    is_active: bool
    base_prompt: str | None = None
    model_name: str | None = None


class AIProviderResponseDTO(BaseMsgspecDTO[AIProviderResponse]):
    pass


class UserProfileResponse(msgspec.Struct):
    id: int
    user_id: int
    ai_auto_process: bool
    ai_provider_id: int
    display_name: str | None = None
    department: str | None = None
    position: str | None = None


class ExternalSystemResponse(msgspec.Struct):
    id: int
    name: str
    display_name: str
    api_config: dict
    is_active: bool


class ExternalSystemResponseDTO(BaseMsgspecDTO[ExternalSystemResponse]):
    pass


class UserProfileUpdateRequest(msgspec.Struct):
    display_name: str | None = None
    department: str | None = None
    position: str | None = None
    ai_auto_process: bool | None = None
    ai_provider_id: int | None = None


class UserProfileUpdateRequestDTO(BaseMsgspecDTO[UserProfileUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")


class AIProviderUpdateRequest(msgspec.Struct):
    name: str | None = None
    base_prompt: str | None = None
    model_name: str | None = None
    requires_api_key: bool | None = None
    is_active: bool | None = None


class AIProviderUpdateRequestDTO(BaseMsgspecDTO[AIProviderUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")


class ExternalSystemUpdateRequest(msgspec.Struct):
    name: str | None = None
    display_name: str | None = None
    api_config: dict | None = None
    is_active: bool | None = None


class ExternalSystemUpdateRequestDTO(BaseMsgspecDTO[ExternalSystemUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")
