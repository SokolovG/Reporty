from uuid import UUID

from litestar import Controller, delete, get, post

from src.api.dto import (
    DailyRecordRequest,
    DailyRecordRequestDTO,
    DailyRecordResponse,
    DailyRecordResponseDTO,
)
from src.api.dto.record_dto import (
    DailyRecordWithTaskResponse,
    DailyRecordWithTaskResponseDTO,
    LinkTaskRequest,
    LinkTaskRequestDTO,
)
from src.services import RecordService


class RecordController(Controller):
    @post(dto=DailyRecordRequestDTO, return_dto=DailyRecordResponseDTO)
    async def create_record(
        self, data: DailyRecordRequest, record_service: RecordService
    ) -> DailyRecordResponse:
        return await record_service.create_record(data)

    @get("/{record_id:uuid}", return_dto=DailyRecordResponseDTO)
    async def get_record(
        self, record_service: RecordService, record_id: UUID
    ) -> DailyRecordResponse:
        return await record_service.get_record(record_id)

    @get("/{record_id:uuid}/with-task", return_dto=DailyRecordWithTaskResponseDTO)
    async def get_record_with_task(
        self, record_service: RecordService, record_id: UUID
    ) -> DailyRecordWithTaskResponse:
        """Get record with full external task information."""
        return await record_service.get_record_with_task(record_id)

    @post(
        "/{record_id:uuid}/link-task",
        dto=LinkTaskRequestDTO,
        return_dto=DailyRecordResponseDTO,
    )
    async def link_external_task(
        self, record_service: RecordService, record_id: UUID, data: LinkTaskRequest
    ) -> DailyRecordResponse:
        """Link record to an external task."""
        return await record_service.link_to_external_task(record_id, data.external_task_id)

    @delete("/{record_id:uuid}/unlink-task", return_dto=DailyRecordResponseDTO)
    async def unlink_external_task(
        self, record_service: RecordService, record_id: UUID
    ) -> DailyRecordResponse:
        """Remove link to external task."""
        return await record_service.unlink_from_external_task(record_id)
