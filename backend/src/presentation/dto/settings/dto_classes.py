from litestar.dto import DTOConfig

from backend.src.presentation.dto.base import BaseMsgspecDTO
from backend.src.presentation.dto.settings.requests import (
    AIPreferencesUpdateRequest,
    AIProviderUpdateRequest,
    ExternalSystemUpdateRequest,
    TaskTypeRequest,
    TaskTypeUpdateRequest,
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
