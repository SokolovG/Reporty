from adaptix.conversion import get_converter

from backend.src.database.models import (
    ExternalSystem,
    User,
    DailyRecord,
    Report,
    TaskType,
    AIModel,
)

from backend.src.api.dto.auth_dto import UserResponse
from backend.src.api.dto.record_dto import DailyRecordResponse
from backend.src.api.dto.report_dto import DailyReportResponse
from backend.src.api.dto.settings_dto import (
    AIPreferencesResponse,
    ExternalSystemResponse,
    TaskTypeResponse,
    AIModelResponse,
)

# Auth converters
user_to_response = get_converter(User, UserResponse)

# Records converters
record_to_response = get_converter(DailyRecord, DailyRecordResponse)

# Reports converters
report_to_response = get_converter(Report, DailyReportResponse)

# Settings converters
to_ai_preferences_response = get_converter(User, AIPreferencesResponse)
ai_model_to_response = get_converter(AIModel, AIModelResponse)
external_system_to_response = get_converter(ExternalSystem, ExternalSystemResponse)
task_type_to_response = get_converter(TaskType, TaskTypeResponse)
