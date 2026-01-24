import msgspec

from backend.src.domain.value_objects import RecordStatus


class DailyRecordData(msgspec.Struct):
    title: str
    raw_input: str
    external_task_url: str | None = None
    external_task_id: int | None = None


class DailyRecordUpdateData(msgspec.Struct):
    title: str | None = None
    text: str | None = None
    external_task_url: str | None = None
    external_task_id: int | None = None


class AppendToRecordData(msgspec.Struct):
    additional_input: str
    separator: str = ","


class LinkTaskData(msgspec.Struct):
    """Request to link record with an external task."""

    external_task_id: int


class RecordStatusUpdateData(msgspec.Struct):
    status: RecordStatus


class ExternalTaskCreateData(msgspec.Struct):
    url: str
    title: str | None = None
    external_id: int | None = None


class ExternalTaskUpdateData(msgspec.Struct):
    url: str | None = None
    title: str | None = None
    external_id: int | None = None
    status: str | None = None
    description: str | None = None
