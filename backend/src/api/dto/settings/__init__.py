from backend.src.api.dto.settings.requests import (
    TaskTypeRequest,
    TaskTypeUpdateRequest,
    AIPreferencesUpdateRequest,
    AIProviderUpdateRequest,
    ExternalSystemUpdateRequest,
)
from backend.src.api.dto.settings.responses import (
    TaskTypeResponse,
    AIPreferencesResponse,
    AIModelResponse,
    AIProviderResponse,
    AISettingsUpdateResponse,
    ExternalSystemResponse,
)
from backend.src.api.dto.settings.dto_classes import (
    TaskTypeRequestDTO,
    TaskTypeUpdateRequestDTO,
    AIPreferencesUpdateRequestDTO,
    AIProviderUpdateRequestDTO,
    ExternalSystemUpdateRequestDTO,
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
