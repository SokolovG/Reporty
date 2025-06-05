from uuid import UUID

from src.api.dto import DailyRecordRequest, DailyRecordResponse
from src.database.repositories import DailyRecordRepository


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
            bitrix_task_id=saved_record.bitrix_task_id,
        )

    async def get_record(self, record_id: UUID) -> DailyRecordResponse:
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
            bitrix_task_id=record.bitrix_task_id,
        )
