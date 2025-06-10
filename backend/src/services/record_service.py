from adaptix.conversion import get_converter

from backend.src.api.dto import DailyRecordRequest, DailyRecordResponse
from backend.src.api.dto.record_dto import DailyRecordWithTaskResponse, ExternalTaskInfo
from backend.src.database.models import DailyRecord
from backend.src.database.repositories import (
    DailyRecordRepository,
    UserSettingsRepository,
)


class RecordService:
    def __init__(
        self, record_repo: DailyRecordRepository, settings_repo: UserSettingsRepository
    ) -> None:
        self.repo = record_repo
        self.settings_repo = settings_repo
        self._to_response = get_converter(DailyRecord, DailyRecordResponse)

    async def create_record(self, data: DailyRecordRequest, user_id: int) -> DailyRecordResponse:
        saved_record = await self.repo.create_record(data)
        settings = await self.settings_repo.get_by_user_id(user_id)

        if settings.ai_auto_process:
            pass
        return self._to_response(saved_record)

    async def get_record(self, record_id: int) -> DailyRecordResponse:
        record = await self.repo.get(record_id)
        return self._to_response(record)

    async def get_record_with_task(self, record_id: int) -> DailyRecordWithTaskResponse:
        """Get record with loaded external task information."""
        record = await self.repo.get(record_id, load=[DailyRecord.external_task])
        external_task_info = None
        if record.external_task:
            external_task_info = ExternalTaskInfo(
                id=record.external_task.id,
                external_id=record.external_task.external_id,
                title=record.external_task.title,
                status=record.external_task.status,
                system_name=record.external_task.system.name,
                system_display_name=record.external_task.system.display_name,
            )

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
            external_task=external_task_info,
        )

    async def link_to_external_task(
        self, record_id: int, external_task_id: int
    ) -> DailyRecordResponse:
        """Link daily record to an external task."""
        record = await self.repo.get(record_id)
        record.external_task_id = external_task_id
        updated_record = await self.repo.update(record)

        return self._to_response(updated_record)

    async def unlink_from_external_task(self, record_id: int) -> DailyRecordResponse:
        """Remove link to external task."""
        record = await self.repo.get(record_id)
        record.external_task_id = None
        updated_record = await self.repo.update(record)

        return self._to_response(updated_record)

    async def process_with_ai(self, record_id: int) -> DailyRecordResponse:  # type: ignore
        pass
