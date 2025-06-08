from backend.src.api.dto import DailyRecordRequest, DailyRecordResponse
from backend.src.api.dto.record_dto import DailyRecordWithTaskResponse
from backend.src.database.models import DailyRecord
from backend.src.database.repositories import DailyRecordRepository


class RecordService:
    def __init__(self, record_repo: DailyRecordRepository) -> None:
        self.repo = record_repo

    async def create_record(self, data: DailyRecordRequest) -> DailyRecordResponse:
        saved_record = await self.repo.create_record(data)

        return DailyRecordResponse(
            id=saved_record.id,
            raw_input=saved_record.raw_input,
            ai_processed=saved_record.ai_processed,
            final_description=saved_record.final_description,
            created_at=saved_record.created_at,
            processed_at=saved_record.processed_at,
            is_processed=saved_record.is_processed,
            is_approved=saved_record.is_approved,
            external_task_id=saved_record.external_task_id,
        )

    async def get_record(self, record_id: int) -> DailyRecordResponse:
        record = await self.repo.get(record_id)
        return DailyRecordResponse(
            id=record.id,
            raw_input=record.raw_input,
            ai_processed=record.ai_processed,
            final_description=record.final_description,
            created_at=record.created_at,
            processed_at=record.processed_at,
            is_processed=record.is_processed,
            is_approved=record.is_approved,
            external_task_id=record.external_task_id,
        )

    async def get_record_with_task(self, record_id: int) -> DailyRecordWithTaskResponse:
        """Get record with loaded external task information."""
        record = await self.repo.get(record_id, load=[DailyRecord.external_task])
        return DailyRecordWithTaskResponse(
            id=record.id,
            raw_input=record.raw_input,
            ai_processed=record.ai_processed,
            final_description=record.final_description,
            created_at=record.created_at,
            processed_at=record.processed_at,
            is_processed=record.is_processed,
            is_approved=record.is_approved,
            external_task_id=record.external_task_id,
        )

    async def link_to_external_task(
        self, record_id: int, external_task_id: int
    ) -> DailyRecordResponse:
        """Link daily record to external task."""
        record = await self.repo.get(record_id)
        record.external_task_id = external_task_id
        updated_record = await self.repo.update(record)

        return DailyRecordResponse(
            id=updated_record.id,
            raw_input=updated_record.raw_input,
            ai_processed=updated_record.ai_processed,
            final_description=updated_record.final_description,
            created_at=updated_record.created_at,
            processed_at=updated_record.processed_at,
            is_processed=updated_record.is_processed,
            is_approved=updated_record.is_approved,
            external_task_id=updated_record.external_task_id,
        )

    async def unlink_from_external_task(self, record_id: int) -> DailyRecordResponse:
        """Remove link to external task."""
        record = await self.repo.get(record_id)
        record.external_task_id = None
        updated_record = await self.repo.update(record)

        return DailyRecordResponse(
            id=updated_record.id,
            raw_input=updated_record.raw_input,
            ai_processed=updated_record.ai_processed,
            final_description=updated_record.final_description,
            created_at=updated_record.created_at,
            processed_at=updated_record.processed_at,
            is_processed=updated_record.is_processed,
            is_approved=updated_record.is_approved,
            external_task_id=updated_record.external_task_id,
        )
