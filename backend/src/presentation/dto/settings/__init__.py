from backend.src.presentation.dto import (
    AIPreferencesUpdateRequest,
    AIProviderUpdateRequest,
    ExternalSystemUpdateRequest,
    TaskTypeRequest,
    TaskTypeUpdateRequest,
)
from backend.src.presentation.dto.settings.dto_classes import (
    AIPreferencesUpdateRequestDTO,
    AIProviderUpdateRequestDTO,
    ExternalSystemUpdateRequestDTO,
    TaskTypeRequestDTO,
    TaskTypeUpdateRequestDTO,
)
from backend.src.presentation.dto.settings.responses import (
    AIModelResponse,
    AIPreferencesResponse,
    AIProviderResponse,
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
    "AIModelResponse",
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
