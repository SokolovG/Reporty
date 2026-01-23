from backend.src.presentation.dto.settings.dto_classes import (
    AIPreferencesUpdateRequestDTO,
    AIProviderUpdateRequestDTO,
    ExternalSystemUpdateRequestDTO,
    TaskTypeRequestDTO,
    TaskTypeUpdateRequestDTO,
)
from backend.src.presentation.dto.settings.responses import (
    AISettingsUpdateResponse,
    ExternalSystemResponse,
    TaskTypeResponse,
)

__all__ = [
    # Requests
    "TaskTypeRequest",
    "TaskTypeUpdateRequest",
    "AIPreferencesUpdateRequest",
    "AIProviderUpdateRequest",
    "ExternalSystemUpdateRequest",
    # Responses
    "TaskTypeResponse",
    "AIPreferencesResponse",
    "AIProviderResponse",
    "AISettingsUpdateResponse",
    "ExternalSystemResponse",
    # DTOs
    "TaskTypeRequestDTO",
    "TaskTypeUpdateRequestDTO",
    "AIPreferencesUpdateRequestDTO",
    "AIProviderUpdateRequestDTO",
    "ExternalSystemUpdateRequestDTO",
]
