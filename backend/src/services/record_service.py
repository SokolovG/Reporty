from datetime import datetime

from adaptix.conversion import get_converter

from backend.src.core.exceptions import InternalServerError, ValidationError
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
    UserRepository,
)


record_to_response = get_converter(DailyRecord, DailyRecordResponse)


class RecordService:
    def __init__(
        self,
        record_repo: DailyRecordRepository,
        user_repository: UserRepository,
    ) -> None:
        self.repo = record_repo
        self.user_repository = user_repository
        self.ai_service = ""

    async def create_record(self, data: DailyRecordRequest, user_id: int) -> DailyRecordResponse:
        """Create a new daily record."""
        try:
            saved_record = await self.repo.create_record(data, user_id)
            user = await self.user_repository.get_one(id=user_id)

            if user.ai_auto_process:
                # ai_processed = await self.ai_service.process(data.raw_input, user_id)
                ai_processed = ""
                saved_record.ai_processed = ai_processed
                updated_record = await self.repo.update(saved_record)
                await self.repo.session.commit()
                return record_to_response(updated_record)

            return record_to_response(saved_record)
        except ValueError as e:
            raise ValidationError(str(e), {"user_id": user_id})
        except Exception as e:
            raise InternalServerError(f"Failed to create record: {str(e)}", {"user_id": user_id})

    async def get_record(self, record_id: int, user_id: int) -> DailyRecordResponse:
        """Get a specific record by ID."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)
            return record_to_response(record)
        except Exception as e:
            raise InternalServerError(f"Failed to get record: {str(e)}", {"record_id": record_id})

    async def get_records(
        self, user_id: int, target_date: datetime | None = None
    ) -> list[DailyRecordResponse]:
        """Get records, optionally filtered by date."""
        try:
            if target_date is not None:
                search_data = (
                    target_date.date() if isinstance(target_date, datetime) else target_date
                )
                records = await self.repo.get_records_by_date(search_data, user_id=user_id)
            else:
                records = await self.repo.get_all_records(user_id=user_id)

            return [record_to_response(record) for record in records]
        except Exception as e:
            raise InternalServerError(f"Failed to get records: {str(e)}")

    async def append_to_record(
        self, record_id: int, user_id: int, data: AppendToRecordRequest
    ) -> DailyRecordResponse:
        """Append additional content to an existing record."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)
            record.raw_input += data.separator + data.additional_input

            updated_record = await self.repo.update(record)
            await self.repo.session.commit()

            return record_to_response(updated_record)
        except Exception as e:
            raise InternalServerError(
                f"Failed to append to record: {str(e)}", {"record_id": record_id}
            )

    async def update_record(
        self, record_id: int, user_id: int, data: DailyRecordUpdateRequest
    ) -> DailyRecordResponse:
        """Update an existing record."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)

            if data.title is not None:
                record.title = data.title
            if data.text is not None:
                record.raw_input = data.text
            if data.external_task_id is not None:
                record.external_task_id = data.external_task_id

            if data.external_task_url is not None:
                # TODO: Find or create task
                record.external_url = data.external_task_url

            updated_record = await self.repo.update(record)
            await self.repo.session.commit()

            return record_to_response(updated_record)
        except Exception as e:
            raise InternalServerError(
                f"Failed to update record: {str(e)}", {"record_id": record_id}
            )

    async def get_record_with_task(
        self, record_id: int, user_id: int
    ) -> DailyRecordWithTaskResponse:
        """Get record with loaded external task information."""
        try:
            record = await self.repo.get_with_external_task(record_id=record_id, user_id=user_id)
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
        except Exception as e:
            raise InternalServerError(
                f"Failed to get record with task: {str(e)}", {"record_id": record_id}
            )

    async def link_to_external_task(
        self, record_id: int, external_task_id: int, user_id: int
    ) -> DailyRecordResponse:
        """Link daily record to an external task."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)
            record.external_task_id = external_task_id
            updated_record = await self.repo.update(record)
            await self.repo.session.commit()

            return record_to_response(updated_record)
        except Exception as e:
            raise InternalServerError(
                f"Failed to link external task: {str(e)}",
                {"record_id": record_id, "external_task_id": external_task_id},
            )

    async def unlink_from_external_task(self, record_id: int, user_id: int) -> DailyRecordResponse:
        """Remove link to external task."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)
            record.external_task_id = None
            updated_record = await self.repo.update(record)
            await self.repo.session.commit()

            return record_to_response(updated_record)
        except Exception as e:
            raise InternalServerError(
                f"Failed to unlink external task: {str(e)}", {"record_id": record_id}
            )

    async def process_with_ai(self, record_id: int, user_id: int) -> DailyRecordResponse:
        """Process record with AI."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)
            # ai_processed = await self.ai_service.process(record.raw_input, user_id)
            ai_processed = ""
            record.ai_processed = ai_processed
            record.processed_at = datetime.now()
            record.is_processed = True

            updated_record = await self.repo.update(record)
            await self.repo.session.commit()

            return record_to_response(updated_record)
        except Exception as e:
            raise InternalServerError(
                f"Failed to process record with AI: {str(e)}",
                {"record_id": record_id, "user_id": user_id},
            )

    async def update_status(
        self, record_id: int, user_id: int, data: RecordStatusUpdateRequest
    ) -> DailyRecordResponse:
        """Update record status."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)
            record.status = data.status.value
            updated_record = await self.repo.update(record)
            await self.repo.session.commit()

            return record_to_response(updated_record)
        except Exception as e:
            raise InternalServerError(
                f"Failed to update record status: {str(e)}", {"record_id": record_id}
            )

    async def delete_record(self, record_id: int, user_id: int) -> None:
        """Delete a record."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)

            await self.repo.delete(record.id)
            await self.repo.session.commit()

        except Exception as e:
            raise InternalServerError(
                f"Failed to delete record: {str(e)}", {"record_id": record_id}
            )

    async def approve_record(self, record_id: int, user_id: int) -> DailyRecordResponse:
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)
            record.is_approved = True
            updated_record = await self.repo.update(record)
            await self.repo.session.commit()
            return record_to_response(updated_record)

        except Exception as e:
            raise InternalServerError(
                f"Failed to approve record: {str(e)}", {"record_id": record_id}
            )
