from adaptix.conversion import get_converter

from backend.src.api.dto import DailyRecordRequest, DailyRecordResponse
from backend.src.api.dto.record_dto import (
    DailyRecordWithTaskResponse,
    ExternalTaskInfo,
    DailyRecordUpdateRequest,
    AppendToRecordRequest,
    RecordStatusUpdateRequest,
)
from backend.src.database.models import DailyRecord
from backend.src.database.repositories import (
    DailyRecordRepository,
    UserProfileRepository,
)
from backend.src.integrations.ai_service import AIService
from backend.src.services import CryptoService


class RecordService:
    def __init__(
        self,
        record_repo: DailyRecordRepository,
        user_profile_settings: UserProfileRepository,
        crypto_service: CryptoService,
    ) -> None:
        self.repo = record_repo
        self.user_profile_settings = user_profile_settings
        self._to_response = get_converter(DailyRecord, DailyRecordResponse)
        self.ai_service = AIService(self.user_profile_settings, crypto_service)

    async def create_record(self, data: DailyRecordRequest, user_id: int) -> DailyRecordResponse:
        saved_record = await self.repo.create_record(data)
        settings = await self.user_profile_settings.get_by_user_id(user_id)

        if settings.ai_auto_process:
            ai_processed = await self.ai_service.process(data.raw_input, user_id)
            saved_record.ai_processed = ai_processed
            updated_record = await self.repo.update(saved_record)
            await self.repo.session.commit()

            return self._to_response(updated_record)

        return self._to_response(saved_record)

    async def get_record(self, record_id: int) -> DailyRecordResponse:
        record = await self.repo.get(record_id)
        return self._to_response(record)

    async def append_to_record(
        self, record_id: int, data: AppendToRecordRequest
    ) -> DailyRecordResponse:
        record = await self.repo.get(record_id)

        record.raw_input += data.separator + data.additional_input

        updated_record = await self.repo.update(record)
        await self.repo.session.commit()

        return self._to_response(updated_record)

    async def update_record(
        self, record_id: int, data: DailyRecordUpdateRequest
    ) -> DailyRecordResponse:
        record = await self.repo.get(record_id)

        if data.title is not None:
            record.title = data.title
        if data.raw_input is not None:
            record.raw_input = data.raw_input
        if data.external_task_id is not None:
            record.external_task_id = data.external_task_id

        if data.external_task_url is not None:
            ...
            # TODO: Find or create task

        updated_record = await self.repo.update(record)
        await self.repo.session.commit()

        return self._to_response(updated_record)

    async def get_record_with_task(self, record_id: int) -> DailyRecordWithTaskResponse:
        """Get record with loaded external task information."""
        record = await self.repo.get_with_external_task(record_id)
        external_task_info = None
        if record.external_task:
            external_task_info = ExternalTaskInfo(
                id=record.external_task.id,
                external_id=record.external_task.external_id,
                title=record.external_task.title or "",
                status=record.external_task.status,
                system_name=record.external_task.system.name,
                system_display_name=record.external_task.system.display_name,
                url=record.external_task.url,
            )

        return DailyRecordWithTaskResponse(
            id=record.id,
            title=record.title,
            raw_input=record.raw_input,
            ai_processed=record.ai_processed,
            final_description=record.final_description,
            created_at=record.created_at,
            processed_at=record.processed_at,
            is_processed=record.is_processed,
            is_approved=record.is_approved,
            external_task_id=record.external_task_id,
            external_task=external_task_info,
            user_id=record.user_id,
        )

    async def link_to_external_task(
        self, record_id: int, external_task_id: int
    ) -> DailyRecordResponse:
        """Link daily record to an external task."""
        record = await self.repo.get(record_id)
        record.external_task_id = external_task_id
        updated_record = await self.repo.update(record)
        await self.repo.session.commit()

        return self._to_response(updated_record)

    async def unlink_from_external_task(self, record_id: int) -> DailyRecordResponse:
        """Remove link to external task."""
        record = await self.repo.get(record_id)
        record.external_task_id = None
        updated_record = await self.repo.update(record)

        return self._to_response(updated_record)

    async def process_with_ai(self, record_id: int, user_id: int) -> DailyRecordResponse:
        record = await self.repo.get(record_id)
        ai_processed = await self.ai_service.process(record.raw_input, user_id)
        record.ai_processed = ai_processed
        updated_record = await self.repo.update(record)
        await self.repo.session.commit()

        return self._to_response(updated_record)

    async def update_status(
        self, record_id: int, data: RecordStatusUpdateRequest
    ) -> DailyRecordResponse:
        record = await self.repo.get(record_id)
        record.status = data.status.value
        updated_record = await self.repo.update(record)
        await self.repo.session.commit()

        return self._to_response(updated_record)
