from litestar.dto import DTOConfig

from backend.src.application.dto.settings import (
    AIPreferencesUpdateData,
    AIProviderUpdateData,
    ExternalSystemUpdateData,
    TaskTypeData,
    TaskTypeUpdateData,
)
from backend.src.presentation.dto.base import BaseMsgspecDTO


class TaskTypeRequestDTO(BaseMsgspecDTO[TaskTypeData]):
    pass


class TaskTypeUpdateRequestDTO(BaseMsgspecDTO[TaskTypeUpdateData]):
    config = DTOConfig(partial=True, rename_strategy="camel")


class AIPreferencesUpdateRequestDTO(BaseMsgspecDTO[AIPreferencesUpdateData]):
    config = DTOConfig(partial=True, rename_strategy="camel")


class AIProviderUpdateRequestDTO(BaseMsgspecDTO[AIProviderUpdateData]):
    config = DTOConfig(partial=True, rename_strategy="camel")


class ExternalSystemUpdateRequestDTO(BaseMsgspecDTO[ExternalSystemUpdateData]):
    config = DTOConfig(partial=True, rename_strategy="camel")
