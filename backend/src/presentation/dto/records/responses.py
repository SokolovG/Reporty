from datetime import datetime

import msgspec


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
    status: str
    external_task_id: int | None
    external_url: str | None = None


class ExternalTaskInfo(msgspec.Struct):
    """Basic external task information for responses."""

    id: int
    external_system_id: int
    title: str
    status: str
    url: str
    external_id: int | None = None
    system_name: str | None = None
    system_display_name: str | None = None


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
    external_url: str | None = None
    external_task: "ExternalTaskInfo | None" = None


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
    user_id: int
