from litestar.dto import DTOConfig

from backend.src.application.dto.records import (
    AppendToRecordData,
    DailyRecordData,
    DailyRecordUpdateData,
    ExternalTaskCreateData,
    ExternalTaskUpdateData,
    LinkTaskData,
    RecordStatusUpdateData,
)
from backend.src.presentation.dto.base import BaseMsgspecDTO
from backend.src.presentation.dto.records.responses import (
    DailyRecordWithTaskResponse,
    ExternalTaskResponse,
)


class DailyRecordRequestDTO(BaseMsgspecDTO[DailyRecordData]):
    pass


class DailyRecordUpdateRequestDTO(BaseMsgspecDTO[DailyRecordUpdateData]):
    pass


class AppendToRecordRequestDTO(BaseMsgspecDTO[AppendToRecordData]):
    pass


class LinkTaskRequestDTO(BaseMsgspecDTO[LinkTaskData]):
    pass


class RecordStatusUpdateRequestDTO(BaseMsgspecDTO[RecordStatusUpdateData]):
    pass


class ExternalTaskCreateRequestDTO(BaseMsgspecDTO[ExternalTaskCreateData]):
    pass


class ExternalTaskUpdateRequestDTO(BaseMsgspecDTO[ExternalTaskUpdateData]):
    config = DTOConfig(partial=True, rename_strategy="camel")


class DailyRecordWithTaskResponseDTO(BaseMsgspecDTO[DailyRecordWithTaskResponse]):
    pass


class ExternalTaskResponseDTO(BaseMsgspecDTO[ExternalTaskResponse]):
    pass
