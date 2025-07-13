from datetime import datetime

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, post, patch, Request
from litestar.params import Parameter

from backend.src.api.dto import (
    DailyRecordRequest,
    DailyRecordRequestDTO,
    DailyRecordResponse,
    DailyRecordResponseDTO,
    RecordStatusUpdateRequest,
    RecordStatusUpdateRequestDTO,
)
from backend.src.api.dto.record_dto import (
    DailyRecordWithTaskResponse,
    DailyRecordWithTaskResponseDTO,
    LinkTaskRequest,
    LinkTaskRequestDTO,
    DailyRecordUpdateRequestDTO,
    DailyRecordUpdateRequest,
    AppendToRecordRequestDTO,
    AppendToRecordRequest,
)
from backend.src.services import RecordService


class RecordController(Controller):
    @post(dto=DailyRecordRequestDTO, return_dto=DailyRecordResponseDTO)
    @inject
    async def create_record(
        self,
        data: DailyRecordRequest,
        request: Request,
        record_service: FromDishka[RecordService],
    ) -> DailyRecordResponse:
        user_id = request.user.id
        return await record_service.create_record(data, user_id)

    @get("/{record_id:int}", return_dto=DailyRecordResponseDTO)
    @inject
    async def get_record(
        self, record_service: FromDishka[RecordService], record_id: int
    ) -> DailyRecordResponse:
        return await record_service.get_record(record_id)

    @get(return_dto=DailyRecordResponseDTO)
    @inject
    async def get_records(
        self,
        record_service: FromDishka[RecordService],
        date: datetime | None = Parameter(
            query="date", default=None, description="Filter records by date (YYYY-MM-DD format)"
        ),
    ) -> list[DailyRecordResponse]:
        return await record_service.get_records(date)

    @patch(
        "/{record_id:int}/status",
        dto=RecordStatusUpdateRequestDTO,
        return_dto=DailyRecordResponseDTO,
    )
    @inject
    async def update_record_status(
        self,
        record_service: FromDishka[RecordService],
        record_id: int,
        data: RecordStatusUpdateRequest,
    ) -> DailyRecordResponse:
        return await record_service.update_status(record_id, data)

    @post(
        "/{record_id:int}/append",
        dto=AppendToRecordRequestDTO,
        return_dto=DailyRecordResponseDTO,
    )
    @inject
    async def append_to_record(
        self,
        data: AppendToRecordRequest,
        record_id: int,
        record_service: FromDishka[RecordService],
    ) -> DailyRecordResponse:
        return await record_service.append_to_record(record_id, data)

    @patch(
        "/{record_id:int}",
        dto=DailyRecordUpdateRequestDTO,
        return_dto=DailyRecordResponseDTO,
    )
    @inject
    async def update_record(
        self,
        data: DailyRecordUpdateRequest,
        record_id: int,
        record_service: FromDishka[RecordService],
    ) -> DailyRecordResponse:
        return await record_service.update_record(record_id, data)

    @get("/{record_id:int}/with-task", return_dto=DailyRecordWithTaskResponseDTO)
    @inject
    async def get_record_with_task(
        self, record_service: FromDishka[RecordService], record_id: int
    ) -> DailyRecordWithTaskResponse:
        """Get record with full external task information."""
        return await record_service.get_record_with_task(record_id)

    @post(
        "/{record_id:int}/link-task",
        dto=LinkTaskRequestDTO,
        return_dto=DailyRecordResponseDTO,
    )
    @inject
    async def link_external_task(
        self,
        record_service: FromDishka[RecordService],
        record_id: int,
        data: LinkTaskRequest,
    ) -> DailyRecordResponse:
        """Link record to an external task."""
        return await record_service.link_to_external_task(record_id, data.external_task_id)

    @delete(
        "/{record_id:int}/unlink-task",
        status_code=200,
        return_dto=DailyRecordResponseDTO,
    )
    @inject
    async def unlink_external_task(
        self, record_service: FromDishka[RecordService], record_id: int
    ) -> DailyRecordResponse:
        """Remove link to external task."""
        return await record_service.unlink_from_external_task(record_id)

    @delete("/{record_id:int}")
    @inject
    async def delete_record(
        self, record_service: FromDishka[RecordService], record_id: int
    ) -> None:
        """Delete record."""
        return await record_service.delete_record(record_id)

    @post("/{record_id:int}/process", return_dto=DailyRecordResponseDTO)
    @inject
    async def process_record_with_ai(
        self, record_service: FromDishka[RecordService], record_id: int, user_id: int
    ) -> DailyRecordResponse:
        """Process record via AI."""
        return await record_service.process_with_ai(record_id, user_id)
