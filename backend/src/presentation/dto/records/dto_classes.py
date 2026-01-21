from litestar.dto import DTOConfig
from backend.src.api.dto.base import BaseMsgspecDTO
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
    DailyRecordWithTaskResponse,
    ExternalTaskResponse,
)


class DailyRecordRequestDTO(BaseMsgspecDTO[DailyRecordRequest]):
    pass


class DailyRecordUpdateRequestDTO(BaseMsgspecDTO[DailyRecordUpdateRequest]):
    pass


class AppendToRecordRequestDTO(BaseMsgspecDTO[AppendToRecordRequest]):
    pass


class LinkTaskRequestDTO(BaseMsgspecDTO[LinkTaskRequest]):
    pass


class RecordStatusUpdateRequestDTO(BaseMsgspecDTO[RecordStatusUpdateRequest]):
    pass


class ExternalTaskCreateRequestDTO(BaseMsgspecDTO[ExternalTaskCreateRequest]):
    pass


class ExternalTaskUpdateRequestDTO(BaseMsgspecDTO[ExternalTaskUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")


class DailyRecordWithTaskResponseDTO(BaseMsgspecDTO[DailyRecordWithTaskResponse]):
    pass


class ExternalTaskResponseDTO(BaseMsgspecDTO[ExternalTaskResponse]):
    pass
