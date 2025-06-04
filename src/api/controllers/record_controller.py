from uuid import UUID

from litestar import Controller, get, post

from src.api.dto import (
    DailyRecordRequest,
    DailyRecordRequestDTO,
    DailyRecordResponse,
    DailyRecordResponseDTO,
)
from src.services.record_service import RecordService


class RecordController(Controller):
    @post("/", dto=DailyRecordRequestDTO, return_dto=DailyRecordResponseDTO)
    async def create_record(
        self, data: DailyRecordRequest, record_service: RecordService
    ) -> DailyRecordResponse:
        return await record_service.create_record(data)

    @get("/{record_id:uuid}", return_dto=DailyRecordResponseDTO)
    async def get_record(
        self, record_service: RecordService, record_id: UUID
    ) -> DailyRecordResponse:
        return await record_service.get_record(record_id)
