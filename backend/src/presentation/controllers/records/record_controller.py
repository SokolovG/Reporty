from datetime import datetime

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, Request, delete, get, patch, post
from litestar.params import Parameter

from backend.src.application.use_cases.records.record_use_cases import RecordUseCases
from backend.src.presentation.dto.records import (
    AppendToRecordRequest,
    AppendToRecordRequestDTO,
    DailyRecordRequest,
    DailyRecordRequestDTO,
    DailyRecordUpdateRequest,
    DailyRecordUpdateRequestDTO,
    LinkTaskRequest,
    LinkTaskRequestDTO,
    RecordStatusUpdateRequest,
    RecordStatusUpdateRequestDTO,
)
from backend.src.presentation.responses.base_responses import SuccessResponse, SuccessResponseDTO


class RecordController(Controller):
    @post(dto=DailyRecordRequestDTO, return_dto=SuccessResponseDTO)
    @inject
    async def create_record(
        self,
        data: DailyRecordRequest,
        request: Request,
        record_use_cases: FromDishka[RecordUseCases],
    ) -> SuccessResponse:
        """Create a new daily record."""
        user_id = request.user.id
        result = await record_use_cases.create(data=data, user_id=user_id)
        return SuccessResponse(message="Record created successfully", data=result)

    @get("/{record_id:int}", return_dto=SuccessResponseDTO)
    @inject
    async def get_record(
        self,
        record_use_cases: FromDishka[RecordUseCases],
        record_id: int,
        request: Request,
    ) -> SuccessResponse:
        """Get a specific record by ID."""
        user_id = request.user.id
        result = await record_use_cases.get(record_id=record_id, user_id=user_id)
        return SuccessResponse(message="Record retrieved successfully", data=result)

    @get(return_dto=SuccessResponseDTO)
    @inject
    async def get_records(
        self,
        record_use_cases: FromDishka[RecordUseCases],
        request: Request,
        date: datetime | None = Parameter(
            query="date", default=None, description="Filter records by date (YYYY-MM-DD format)"
        ),
    ) -> SuccessResponse:
        """Get all records for user."""
        user_id = request.user.id
        result = await record_use_cases.get_many(target_date=date, user_id=user_id)
        return SuccessResponse(message="Records retrieved successfully", data=result)

    @patch(
        "/{record_id:int}/status",
        dto=RecordStatusUpdateRequestDTO,
        return_dto=SuccessResponseDTO,
    )
    @inject
    async def update_record_status(
        self,
        record_use_cases: FromDishka[RecordUseCases],
        record_id: int,
        request: Request,
        data: RecordStatusUpdateRequest,
    ) -> SuccessResponse:
        """Update record status."""
        user_id = request.user.id
        result = await record_use_cases.update_status(
            record_id=record_id, data=data, user_id=user_id
        )
        return SuccessResponse(message="Record status updated successfully", data=result)

    @post(
        "/{record_id:int}/append",
        dto=AppendToRecordRequestDTO,
        return_dto=SuccessResponseDTO,
    )
    @inject
    async def append_to_record(
        self,
        data: AppendToRecordRequest,
        record_id: int,
        request: Request,
        record_use_cases: FromDishka[RecordUseCases],
    ) -> SuccessResponse:
        """Append content to existing record."""
        user_id = request.user.id
        result = await record_use_cases.append(record_id=record_id, data=data, user_id=user_id)
        return SuccessResponse(message="Content appended to record successfully", data=result)

    @patch(
        "/{record_id:int}",
        dto=DailyRecordUpdateRequestDTO,
        return_dto=SuccessResponseDTO,
    )
    @inject
    async def update_record(
        self,
        data: DailyRecordUpdateRequest,
        record_id: int,
        request: Request,
        record_use_cases: FromDishka[RecordUseCases],
    ) -> SuccessResponse:
        """Update an existing record."""
        user_id = request.user.id
        result = await record_use_cases.update(record_id=record_id, data=data, user_id=user_id)
        return SuccessResponse(message="Record updated successfully", data=result)

    @get("/{record_id:int}/with-task", return_dto=SuccessResponseDTO)
    @inject
    async def get_record_with_task(
        self, record_use_cases: FromDishka[RecordUseCases], record_id: int, request: Request
    ) -> SuccessResponse:
        """Get record with external task information."""
        user_id = request.user.id
        result = await record_use_cases.get_with_task(record_id=record_id, user_id=user_id)
        return SuccessResponse(message="Record with task retrieved successfully", data=result)

    @post(
        "/{record_id:int}/link-task",
        dto=LinkTaskRequestDTO,
        return_dto=SuccessResponseDTO,
    )
    @inject
    async def link_external_task(
        self,
        record_use_cases: FromDishka[RecordUseCases],
        record_id: int,
        request: Request,
        data: LinkTaskRequest,
    ) -> SuccessResponse:
        """Link record to external task."""
        user_id = request.user.id
        result = await record_use_cases.link_task(
            record_id=record_id, external_task_id=data.external_task_id, user_id=user_id
        )
        return SuccessResponse(message="Record linked to external task successfully", data=result)

    @delete(
        "/{record_id:int}/unlink-task",
        status_code=200,
        return_dto=SuccessResponseDTO,
    )
    @inject
    async def unlink_external_task(
        self, record_use_cases: FromDishka[RecordUseCases], record_id: int, request: Request
    ) -> SuccessResponse:
        """Unlink external task from record."""
        user_id = request.user.id
        result = await record_use_cases.unlink_from_external_task(
            record_id=record_id, user_id=user_id
        )
        return SuccessResponse(message="External task unlinked successfully", data=result)

    @delete("/{record_id:int}")
    @inject
    async def delete_record(
        self, record_use_cases: FromDishka[RecordUseCases], record_id: int, request: Request
    ) -> None:
        """Delete a record."""
        user_id = request.user.id
        await record_use_cases.delete(record_id=record_id, user_id=user_id)

    @post("/{record_id:int}/process", return_dto=SuccessResponseDTO)
    @inject
    async def process_record_with_ai(
        self, record_use_cases: FromDishka[RecordUseCases], record_id: int, request: Request
    ) -> SuccessResponse:
        """Process record with AI."""
        user_id = request.user.id
        result = await record_use_cases.process_with_ai(record_id=record_id, user_id=user_id)
        return SuccessResponse(message="Record processed with AI successfully", data=result)

    @post("/{record_id: int}/approve", return_dto=SuccessResponseDTO)
    @inject
    async def approve_record(
        self, record_use_cases: FromDishka[RecordUseCases], record_id: int, request: Request
    ) -> SuccessResponse:
        """Approve processed record."""
        user_id = request.user.id
        result = await record_use_cases.approve(record_id=record_id, user_id=user_id)
        return SuccessResponse(message="Record approved successfully", data=result)
