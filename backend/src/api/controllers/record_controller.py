from litestar import Controller, delete, get, post

from backend.src.api.dto import (
    DailyRecordRequest,
    DailyRecordRequestDTO,
    DailyRecordResponse,
    DailyRecordResponseDTO,
)
from backend.src.api.dto.record_dto import (
    DailyRecordWithTaskResponse,
    DailyRecordWithTaskResponseDTO,
    LinkTaskRequest,
    LinkTaskRequestDTO,
)
from backend.src.services import RecordService


class RecordController(Controller):
    @post(dto=DailyRecordRequestDTO, return_dto=DailyRecordResponseDTO)
    async def create_record(
        self, data: DailyRecordRequest, record_service: RecordService
    ) -> DailyRecordResponse:
        return await record_service.create_record(data)

    @get("/{record_id:int}", return_dto=DailyRecordResponseDTO)
    async def get_record(
        self, record_service: RecordService, record_id: int
    ) -> DailyRecordResponse:
        return await record_service.get_record(record_id)

    @get("/{record_id:int}/with-task", return_dto=DailyRecordWithTaskResponseDTO)
    async def get_record_with_task(
        self, record_service: RecordService, record_id: int
    ) -> DailyRecordWithTaskResponse:
        """Get record with full external task information."""
        return await record_service.get_record_with_task(record_id)

    @post(
        "/{record_id:int}/link-task",
        dto=LinkTaskRequestDTO,
        return_dto=DailyRecordResponseDTO,
    )
    async def link_external_task(
        self, record_service: RecordService, record_id: int, data: LinkTaskRequest
    ) -> DailyRecordResponse:
        """Link record to an external task."""
        return await record_service.link_to_external_task(record_id, data.external_task_id)

    @delete(
        "/{record_id:int}/unlink-task",
        status_code=200,
        return_dto=DailyRecordResponseDTO,
    )
    async def unlink_external_task(
        self, record_service: RecordService, record_id: int
    ) -> DailyRecordResponse:
        """Remove link to external task."""
        return await record_service.unlink_from_external_task(record_id)
