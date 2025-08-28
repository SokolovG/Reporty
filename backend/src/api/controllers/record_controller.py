from datetime import datetime
from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, post, patch, Request
from litestar.params import Parameter

from backend.src.api.dto import (
    DailyRecordRequest,
    DailyRecordRequestDTO,
    RecordStatusUpdateRequest,
    RecordStatusUpdateRequestDTO,
)
from backend.src.api.dto.record_dto import (
    LinkTaskRequest,
    LinkTaskRequestDTO,
    DailyRecordUpdateRequestDTO,
    DailyRecordUpdateRequest,
    AppendToRecordRequestDTO,
    AppendToRecordRequest,
)
from backend.src.services import RecordService
from backend.src.api.responses.base_responses import SuccessResponse, SuccessResponseDTO


class RecordController(Controller):
    @post(dto=DailyRecordRequestDTO, return_dto=SuccessResponseDTO)
    @inject
    async def create_record(
        self,
        data: DailyRecordRequest,
        request: Request,
        record_service: FromDishka[RecordService],
    ) -> SuccessResponse:
        """

        Raises:
            ValidationError
            InternalServerError
        """
        user_id = request.user.id
        result = await record_service.create_record(data=data, user_id=user_id)
        return SuccessResponse(message="Record created successfully", data=result)

    @get("/{record_id:int}", return_dto=SuccessResponseDTO)
    @inject
    async def get_record(
        self, record_service: FromDishka[RecordService], record_id: int
    ) -> SuccessResponse:
        """
        Raises:
            NotFoundError
            InternalServerError
        """
        result = await record_service.get_record(record_id)
        return SuccessResponse(message="Record retrieved successfully", data=result)

    @get(return_dto=SuccessResponseDTO)
    @inject
    async def get_records(
        self,
        record_service: FromDishka[RecordService],
        request: Request,
        date: datetime | None = Parameter(
            query="date", default=None, description="Filter records by date (YYYY-MM-DD format)"
        ),
    ) -> SuccessResponse:
        """
        Raises:
            InternalServerError
        """
        user_id = request.user.id
        result = await record_service.get_records(target_date=date, user_id=user_id)
        return SuccessResponse(message="Records retrieved successfully", data=result)

    @patch(
        "/{record_id:int}/status",
        dto=RecordStatusUpdateRequestDTO,
        return_dto=SuccessResponseDTO,
    )
    @inject
    async def update_record_status(
        self,
        record_service: FromDishka[RecordService],
        record_id: int,
        data: RecordStatusUpdateRequest,
    ) -> SuccessResponse:
        """
        Raises:
            NotFoundError
            InternalServerError
        """
        result = await record_service.update_status(record_id, data)
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
        record_service: FromDishka[RecordService],
    ) -> SuccessResponse:
        """
        Raises:
            NotFoundError
            InternalServerError
        """
        result = await record_service.append_to_record(record_id, data)
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
        record_service: FromDishka[RecordService],
    ) -> SuccessResponse:
        """
        Raises:
            NotFoundError
            InternalServerError
        """
        result = await record_service.update_record(record_id, data)
        return SuccessResponse(message="Record updated successfully", data=result)

    @get("/{record_id:int}/with-task", return_dto=SuccessResponseDTO)
    @inject
    async def get_record_with_task(
        self, record_service: FromDishka[RecordService], record_id: int
    ) -> SuccessResponse:
        """
        Raises:
            NotFoundError
            InternalServerError
        """
        result = await record_service.get_record_with_task(record_id)
        return SuccessResponse(message="Record with task retrieved successfully", data=result)

    @post(
        "/{record_id:int}/link-task",
        dto=LinkTaskRequestDTO,
        return_dto=SuccessResponseDTO,
    )
    @inject
    async def link_external_task(
        self,
        record_service: FromDishka[RecordService],
        record_id: int,
        data: LinkTaskRequest,
    ) -> SuccessResponse:
        """
        Raises:
            NotFoundError
            InternalServerError
        """
        result = await record_service.link_to_external_task(record_id, data.external_task_id)
        return SuccessResponse(message="Record linked to external task successfully", data=result)

    @delete(
        "/{record_id:int}/unlink-task",
        status_code=200,
        return_dto=SuccessResponseDTO,
    )
    @inject
    async def unlink_external_task(
        self, record_service: FromDishka[RecordService], record_id: int
    ) -> SuccessResponse:
        """
        Raises:
            NotFoundError
            InternalServerError
        """
        result = await record_service.unlink_from_external_task(record_id)
        return SuccessResponse(message="External task unlinked successfully", data=result)

    @delete("/{record_id:int}")
    @inject
    async def delete_record(
        self, record_service: FromDishka[RecordService], record_id: int
    ) -> None:
        """
        Raises:
            NotFoundError
            InternalServerError
        """
        await record_service.delete_record(record_id)

    @post("/{record_id:int}/process", return_dto=SuccessResponseDTO)
    @inject
    async def process_record_with_ai(
        self, record_service: FromDishka[RecordService], record_id: int, request: Request
    ) -> SuccessResponse:
        """
        Raises:
            NotFoundError
            InternalServerError
        """
        user_id = request.user.id
        result = await record_service.process_with_ai(record_id, user_id)
        return SuccessResponse(message="Record processed with AI successfully", data=result)
