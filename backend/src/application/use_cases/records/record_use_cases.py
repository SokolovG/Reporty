from datetime import datetime

from backend.src.application.dto.records import (
    AppendToRecordData,
    DailyRecordData,
    DailyRecordUpdateData,
    RecordStatusUpdateData,
)
from backend.src.application.use_cases.ai.ai_use_cases import AIUseCases
from backend.src.domain.entities.record import DailyRecord
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.repositories import DailyRecordRepository, UserRepository
from backend.src.infrastructure.exceptions.api_exceptions import (
    InternalServerError,
    ValidationError,
)


class RecordUseCases:
    def __init__(
        self,
        record_repo: DailyRecordRepository,
        user_repository: UserRepository,
        converter: Converter,
        ai_use_cases: AIUseCases | None = None,
    ) -> None:
        self.repo = record_repo
        self.user_repository = user_repository
        self.ai_use_cases = ai_use_cases
        self.convertor = converter

    async def create(self, data: DailyRecordData, user_id: int) -> DailyRecord:
        """Create a new daily record."""
        try:
            saved_record = await self.repo.create_record(data, user_id)
            user = await self.user_repository.get_one(id=user_id)

            if user.ai_auto_process and self.ai_use_cases:
                try:
                    ai_processed = await self.ai_use_cases.process_record(data.raw_input, user_id)
                    saved_record.ai_processed = ai_processed
                    saved_record.is_processed = True
                    saved_record.processed_at = datetime.now()
                    updated_record = await self.repo.update(saved_record)
                    await self.repo.session.commit()
                    return updated_record
                except Exception:
                    # If AI processing fails, continue without it
                    pass

            domain_record = self.convertor.convert(saved_record, DailyRecord)
            return domain_record

        except ValueError as e:
            raise ValidationError(str(e), {"user_id": user_id})
        except Exception as e:
            raise InternalServerError(f"Failed to create record: {str(e)}", {"user_id": user_id})

    async def get(self, record_id: int, user_id: int) -> DailyRecord:
        """Get a specific record by ID."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)
            return self.convertor.convert(record, DailyRecord)
        except Exception as e:
            raise InternalServerError(f"Failed to get record: {str(e)}", {"record_id": record_id})

    async def get_many(
        self, user_id: int, target_date: datetime | None = None
    ) -> list[DailyRecord]:
        """Get records, optionally filtered by date."""
        try:
            if target_date is not None:
                search_data = (
                    target_date.date() if isinstance(target_date, datetime) else target_date
                )
                records = await self.repo.get_records_by_date(search_data, user_id=user_id)
            else:
                records = await self.repo.get_all_records(user_id=user_id)

            return [self.convertor.convert(record, DailyRecord) for record in records]

        except Exception as e:
            raise InternalServerError(f"Failed to get records: {str(e)}")

    async def append(self, record_id: int, user_id: int, data: AppendToRecordData) -> DailyRecord:
        """Append additional content to an existing record."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)
            record.raw_input += data.separator + data.additional_input

            updated_record = await self.repo.update(record)
            await self.repo.session.commit()

            return self.convertor.convert(updated_record, DailyRecord)
        except Exception as e:
            raise InternalServerError(
                f"Failed to append to record: {str(e)}", {"record_id": record_id}
            )

    async def update(
        self, record_id: int, user_id: int, data: DailyRecordUpdateData
    ) -> DailyRecord:
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

            return self.convertor.convert(updated_record, DailyRecord)
        except Exception as e:
            raise InternalServerError(
                f"Failed to update record: {str(e)}", {"record_id": record_id}
            )

    async def get_with_task(self, record_id: int, user_id: int) -> DailyRecord:
        """Get record with loaded external task information."""
        try:
            record = await self.repo.get_with_external_task(record_id=record_id, user_id=user_id)
            return self.convertor.convert(record, DailyRecord)
        except Exception as e:
            raise InternalServerError(
                f"Failed to get record with task: {str(e)}", {"record_id": record_id}
            )

    async def link_task(self, record_id: int, external_task_id: int, user_id: int) -> DailyRecord:
        """Link daily record to an external task."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)
            record.external_task_id = external_task_id
            updated_record = await self.repo.update(record)
            await self.repo.session.commit()

            return self.convertor.convert(updated_record, DailyRecord)
        except Exception as e:
            raise InternalServerError(
                f"Failed to link external task: {str(e)}",
                {"record_id": record_id, "external_task_id": external_task_id},
            )

    async def unlink_from_external_task(self, record_id: int, user_id: int) -> DailyRecord:
        """Remove link to external task."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)
            record.external_task_id = None
            updated_record = await self.repo.update(record)
            await self.repo.session.commit()
            return self.convertor.convert(updated_record, DailyRecord)

        except Exception as e:
            raise InternalServerError(
                f"Failed to unlink external task: {str(e)}", {"record_id": record_id}
            )

    async def update_status(
        self, record_id: int, user_id: int, data: RecordStatusUpdateData
    ) -> DailyRecord:
        """Update record status."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)
            record.status = data.status.value
            updated_record = await self.repo.update(record)
            await self.repo.session.commit()

            return self.convertor.convert(updated_record, DailyRecord)

        except Exception as e:
            raise InternalServerError(
                f"Failed to update record status: {str(e)}", {"record_id": record_id}
            )

    async def delete(self, record_id: int, user_id: int) -> None:
        """Delete a record."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)

            await self.repo.delete(record.id)
            await self.repo.session.commit()

        except Exception as e:
            raise InternalServerError(
                f"Failed to delete record: {str(e)}", {"record_id": record_id}
            )

    async def approve(self, record_id: int, user_id: int) -> DailyRecord:
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)
            record.is_approved = True
            updated_record = await self.repo.update(record)
            await self.repo.session.commit()
            return self.convertor.convert(updated_record, DailyRecord)

        except Exception as e:
            raise InternalServerError(
                f"Failed to approve record: {str(e)}", {"record_id": record_id}
            )

    async def process_with_ai(self, record_id: int, user_id: int) -> DailyRecord:
        """Process record with AI."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)

            if not self.ai_use_cases:
                raise InternalServerError("AI service not available")

            ai_processed = await self.ai_use_cases.process_record(record.raw_input, user_id)
            record.ai_processed = ai_processed
            record.processed_at = datetime.now()
            record.is_processed = True

            updated_record = await self.repo.update(record)
            await self.repo.session.commit()

            return self.convertor.convert(updated_record, DailyRecord)

        except Exception as e:
            raise InternalServerError(
                f"Failed to process record with AI: {str(e)}",
                {"record_id": record_id, "user_id": user_id},
            )
