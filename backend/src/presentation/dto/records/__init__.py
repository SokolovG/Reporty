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
from backend.src.presentation.dto.records.responses import (
    DailyRecordResponse,
    DailyRecordWithTaskResponse,
    ExternalTaskInfo,
    ExternalTaskResponse,
)

__all__ = [
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
