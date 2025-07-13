from datetime import datetime

import msgspec
from litestar.dto import DTOConfig, MsgspecDTO

from backend.src.database.base import RecordStatus


class DailyRecordRequest(msgspec.Struct):
    title: str
    raw_input: str
    external_task_url: str | None = None
    external_task_id: int | None = None


class DailyRecordUpdateRequest(msgspec.Struct):
    title: str | None = None
    raw_input: str | None = None
    external_task_url: str | None = None
    external_task_id: int | None = None


class AppendToRecordRequest(msgspec.Struct):
    additional_input: str
    separator: str = ","


class DailyRecordResponse(msgspec.Struct):
    id: int
    user_id: int
    title: str
    raw_input: str
    ai_processed: str | None
    final_description: str | None
    created_at: datetime
    processed_at: datetime | None
    is_processed: bool
    is_approved: bool
    external_task_id: int | None


class DailyRecordWithTaskResponse(msgspec.Struct):
    """Response with external task information included."""

    id: int
    user_id: int
    title: str
    raw_input: str
    ai_processed: str | None
    final_description: str | None
    created_at: datetime
    processed_at: datetime | None
    is_processed: bool
    is_approved: bool
    external_task_id: int | None
    external_task: "ExternalTaskInfo | None" = None


class ExternalTaskInfo(msgspec.Struct):
    """Basic external task information for responses."""

    id: int
    title: str
    status: str
    system_name: str
    system_display_name: str
    url: str
    external_id: int | None = None


class LinkTaskRequest(msgspec.Struct):
    """Request to link record with an external task."""

    external_task_id: int


class RecordStatusUpdateRequest(msgspec.Struct):
    status: RecordStatus


class DailyRecordRequestDTO(MsgspecDTO[DailyRecordRequest]):
    config = DTOConfig()


class DailyRecordUpdateRequestDTO(MsgspecDTO[DailyRecordUpdateRequest]):
    config = DTOConfig()


class AppendToRecordRequestDTO(MsgspecDTO[AppendToRecordRequest]):
    config = DTOConfig()


class DailyRecordResponseDTO(MsgspecDTO[DailyRecordResponse]):
    config = DTOConfig()


class DailyRecordWithTaskResponseDTO(MsgspecDTO[DailyRecordWithTaskResponse]):
    config = DTOConfig()


class LinkTaskRequestDTO(MsgspecDTO[LinkTaskRequest]):
    config = DTOConfig()


class ExternalTaskCreateRequest(msgspec.Struct):
    url: str
    title: str | None = None
    external_id: int | None = None


class ExternalTaskUpdateRequest(msgspec.Struct):
    url: str | None = None
    title: str | None = None
    external_id: int | None = None
    status: str | None = None
    description: str | None = None


class ExternalTaskCreateRequestDTO(MsgspecDTO[ExternalTaskCreateRequest]):
    config = DTOConfig()


class ExternalTaskUpdateRequestDTO(MsgspecDTO[ExternalTaskUpdateRequest]):
    config = DTOConfig(partial=True)


class ExternalTaskResponse(msgspec.Struct):
    id: int
    external_id: int | None
    external_system_id: int
    title: str | None
    description: str | None
    status: str
    url: str
    external_created_at: datetime
    external_updated_at: datetime | None
    completed_at: datetime | None
    last_sync: datetime


class ExternalTaskResponseDTO(MsgspecDTO[ExternalTaskResponse]):
    config = DTOConfig()


class RecordStatusUpdateRequestDTO(MsgspecDTO[RecordStatusUpdateRequest]):
    config = DTOConfig()
