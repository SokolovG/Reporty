from litestar.dto import DTOConfig
from backend.src.api.dto.base import BaseMsgspecDTO
from backend.src.api.dto.settings.requests import (
    TaskTypeRequest,
    TaskTypeUpdateRequest,
    AIPreferencesUpdateRequest,
    AIProviderUpdateRequest,
    ExternalSystemUpdateRequest,
)


class TaskTypeRequestDTO(BaseMsgspecDTO[TaskTypeRequest]):
    pass


class TaskTypeUpdateRequestDTO(BaseMsgspecDTO[TaskTypeUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")


class AIPreferencesUpdateRequestDTO(BaseMsgspecDTO[AIPreferencesUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")


class AIProviderUpdateRequestDTO(BaseMsgspecDTO[AIProviderUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")


class ExternalSystemUpdateRequestDTO(BaseMsgspecDTO[ExternalSystemUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")
