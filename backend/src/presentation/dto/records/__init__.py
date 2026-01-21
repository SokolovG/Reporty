from backend.src.api.dto.records.requests import (
    DailyRecordRequest,
    DailyRecordUpdateRequest,
    AppendToRecordRequest,
    LinkTaskRequest,
    RecordStatusUpdateRequest,
    ExternalTaskCreateRequest,
    ExternalTaskUpdateRequest,
)
from backend.src.api.dto.records.responses import (
    DailyRecordResponse,
    DailyRecordWithTaskResponse,
    ExternalTaskInfo,
    ExternalTaskResponse,
)
from backend.src.api.dto.records.dto_classes import (
    DailyRecordRequestDTO,
    DailyRecordUpdateRequestDTO,
    AppendToRecordRequestDTO,
    LinkTaskRequestDTO,
    RecordStatusUpdateRequestDTO,
    ExternalTaskCreateRequestDTO,
    ExternalTaskUpdateRequestDTO,
    DailyRecordWithTaskResponseDTO,
    ExternalTaskResponseDTO,
)

__all__ = [
    # Requests
    "DailyRecordRequest",
    "DailyRecordUpdateRequest",
    "AppendToRecordRequest",
    "LinkTaskRequest",
    "RecordStatusUpdateRequest",
    "ExternalTaskCreateRequest",
    "ExternalTaskUpdateRequest",
    # Responses
    "DailyRecordResponse",
    "DailyRecordWithTaskResponse",
    "ExternalTaskInfo",
    "ExternalTaskResponse",
    # DTOs
    "DailyRecordRequestDTO",
    "DailyRecordUpdateRequestDTO",
    "AppendToRecordRequestDTO",
    "LinkTaskRequestDTO",
    "RecordStatusUpdateRequestDTO",
    "ExternalTaskCreateRequestDTO",
    "ExternalTaskUpdateRequestDTO",
    "DailyRecordWithTaskResponseDTO",
    "ExternalTaskResponseDTO",
]
