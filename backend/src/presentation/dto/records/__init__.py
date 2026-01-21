from backend.src.presentation.dto.records.dto_classes import (
    AppendToRecordRequestDTO,
    DailyRecordRequestDTO,
    DailyRecordUpdateRequestDTO,
    DailyRecordWithTaskResponseDTO,
    ExternalTaskCreateRequestDTO,
    ExternalTaskResponseDTO,
    ExternalTaskUpdateRequestDTO,
    LinkTaskRequestDTO,
    RecordStatusUpdateRequestDTO,
)
from backend.src.presentation.dto.records.requests import (
    AppendToRecordRequest,
    DailyRecordRequest,
    DailyRecordUpdateRequest,
    ExternalTaskCreateRequest,
    ExternalTaskUpdateRequest,
    LinkTaskRequest,
    RecordStatusUpdateRequest,
)
from backend.src.presentation.dto.records.responses import (
    DailyRecordResponse,
    DailyRecordWithTaskResponse,
    ExternalTaskInfo,
    ExternalTaskResponse,
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
