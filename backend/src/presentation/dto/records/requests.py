import msgspec
from backend.src.database.base import RecordStatus


class DailyRecordRequest(msgspec.Struct):
    title: str
    raw_input: str
    external_task_url: str | None = None
    external_task_id: int | None = None


class DailyRecordUpdateRequest(msgspec.Struct):
    title: str | None = None
    text: str | None = None
    external_task_url: str | None = None
    external_task_id: int | None = None


class AppendToRecordRequest(msgspec.Struct):
    additional_input: str
    separator: str = ","


class LinkTaskRequest(msgspec.Struct):
    """Request to link record with an external task."""

    external_task_id: int


class RecordStatusUpdateRequest(msgspec.Struct):
    status: RecordStatus


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
