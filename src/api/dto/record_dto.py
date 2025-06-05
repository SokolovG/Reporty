from datetime import datetime

import msgspec
from litestar.dto import DTOConfig, MsgspecDTO


class DailyRecordRequest(msgspec.Struct):
    raw_input: str
    external_task_id: int | None = None


class DailyRecordResponse(msgspec.Struct):
    id: int
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
    external_id: int
    title: str
    status: str
    system_name: str
    system_display_name: str


class LinkTaskRequest(msgspec.Struct):
    """Request to link record with an external task."""

    external_task_id: int


class DailyRecordRequestDTO(MsgspecDTO[DailyRecordRequest]):
    config = DTOConfig()


class DailyRecordResponseDTO(MsgspecDTO[DailyRecordResponse]):
    config = DTOConfig()


class DailyRecordWithTaskResponseDTO(MsgspecDTO[DailyRecordWithTaskResponse]):
    config = DTOConfig()


class LinkTaskRequestDTO(MsgspecDTO[LinkTaskRequest]):
    config = DTOConfig()
