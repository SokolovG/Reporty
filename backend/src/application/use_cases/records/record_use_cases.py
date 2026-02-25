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
from backend.src.infrastructure.database.models import DailyRecordModel
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
        self.converter = converter

    async def create(self, data: DailyRecordData, user_id: int) -> DailyRecord:
        """Create a new daily record."""
        try:
            model = await self.repo.create_record(data, user_id)

            entity = self.converter.convert(model, DailyRecord)

            user_model = await self.user_repository.get_one(id=user_id)
            from backend.src.domain.entities.user import User

            user_entity = self.converter.convert(user_model, User)

            if user_entity.ai_auto_process and self.ai_use_cases:
                try:
                    ai_result = await self.ai_use_cases.process_record(entity.raw_input, user_id)
                    entity.mark_as_processed(ai_result)

                    updated_model = self.converter.convert(entity, DailyRecordModel)
                    updated_model.id = model.id  # Keep ID

                    saved_model = await self.repo.update(updated_model)
                    await self.repo.session.commit()
                    return self.converter.convert(saved_model, DailyRecord)
                except Exception:
                    pass

            return entity

        except ValueError as e:
            raise ValidationError(str(e), {"user_id": user_id})
        except Exception as e:
            raise InternalServerError(f"Failed to create record: {str(e)}", {"user_id": user_id})

    async def get(self, record_id: int, user_id: int) -> DailyRecord:
        """Get a specific record by ID."""
        try:
            model = await self.repo.get_record(record_id=record_id, user_id=user_id)
            return self.converter.convert(model, DailyRecord)
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
                models = await self.repo.get_records_by_date(search_data, user_id=user_id)
            else:
                models = await self.repo.get_all_records(user_id=user_id)

            return [self.converter.convert(model, DailyRecord) for model in models]

        except Exception as e:
            raise InternalServerError(f"Failed to get records: {str(e)}")

    async def append(self, record_id: int, user_id: int, data: AppendToRecordData) -> DailyRecord:
        """Append additional content to an existing record."""
        try:
            model = await self.repo.get_record(record_id=record_id, user_id=user_id)
            entity = self.converter.convert(model, DailyRecord)

            entity.raw_input = f"{entity.raw_input}{data.separator}{data.additional_input}"
            entity.is_processed = False
            entity.ai_processed = None

            updated_model = self.converter.convert(entity, DailyRecordModel)
            updated_model.id = model.id

            saved_model = await self.repo.update(updated_model)
            await self.repo.session.commit()

            return self.converter.convert(saved_model, DailyRecord)
        except Exception as e:
            raise InternalServerError(
                f"Failed to append to record: {str(e)}", {"record_id": record_id}
            )

    async def update(
        self, record_id: int, user_id: int, data: DailyRecordUpdateData
    ) -> DailyRecord:
        """Update an existing record."""
        try:
            model = await self.repo.get_record(record_id=record_id, user_id=user_id)
            entity = self.converter.convert(model, DailyRecord)

            if data.title is not None:
                entity.title = data.title
            if data.text is not None:
                entity.raw_input = data.text
                entity.is_processed = False
                entity.ai_processed = None

            if data.external_task_id is not None:
                entity.link_external_task(data.external_task_id, data.external_task_url)

            updated_model = self.converter.convert(entity, DailyRecordModel)
            updated_model.id = model.id

            saved_model = await self.repo.update(updated_model)
            await self.repo.session.commit()

            return self.converter.convert(saved_model, DailyRecord)
        except Exception as e:
            raise InternalServerError(
                f"Failed to update record: {str(e)}", {"record_id": record_id}
            )

    async def get_with_task(self, record_id: int, user_id: int) -> DailyRecord:
        """Get record with loaded external task information."""
        try:
            model = await self.repo.get_with_external_task(record_id=record_id, user_id=user_id)
            return self.converter.convert(model, DailyRecord)
        except Exception as e:
            raise InternalServerError(
                f"Failed to get record with task: {str(e)}", {"record_id": record_id}
            )

    async def link_task(self, record_id: int, external_task_id: int, user_id: int) -> DailyRecord:
        """Link daily record to an external task."""
        try:
            model = await self.repo.get_record(record_id=record_id, user_id=user_id)
            entity = self.converter.convert(model, DailyRecord)

            entity.link_external_task(external_task_id)

            updated_model = self.converter.convert(entity, DailyRecordModel)
            updated_model.id = model.id

            saved_model = await self.repo.update(updated_model)
            await self.repo.session.commit()

            return self.converter.convert(saved_model, DailyRecord)
        except Exception as e:
            raise InternalServerError(
                f"Failed to link external task: {str(e)}",
                {"record_id": record_id, "external_task_id": external_task_id},
            )

    async def unlink_from_external_task(self, record_id: int, user_id: int) -> DailyRecord:
        """Remove link to external task."""
        try:
            model = await self.repo.get_record(record_id=record_id, user_id=user_id)
            entity = self.converter.convert(model, DailyRecord)

            entity.unlink_external_task()

            updated_model = self.converter.convert(entity, DailyRecordModel)
            updated_model.id = model.id

            saved_model = await self.repo.update(updated_model)
            await self.repo.session.commit()
            return self.converter.convert(saved_model, DailyRecord)

        except Exception as e:
            raise InternalServerError(
                f"Failed to unlink external task: {str(e)}", {"record_id": record_id}
            )

    async def update_status(
        self, record_id: int, user_id: int, data: RecordStatusUpdateData
    ) -> DailyRecord:
        """Update record status."""
        try:
            model = await self.repo.get_record(record_id=record_id, user_id=user_id)
            entity = self.converter.convert(model, DailyRecord)

            if data.status.value == "CLOSED":
                entity.close()
            else:
                entity.reopen()

            updated_model = self.converter.convert(entity, DailyRecordModel)
            updated_model.id = model.id

            saved_model = await self.repo.update(updated_model)
            await self.repo.session.commit()

            return self.converter.convert(saved_model, DailyRecord)

        except Exception as e:
            raise InternalServerError(
                f"Failed to update record status: {str(e)}", {"record_id": record_id}
            )

    async def delete(self, record_id: int, user_id: int) -> None:
        """Delete a record."""
        try:
            model = await self.repo.get_record(record_id=record_id, user_id=user_id)

            await self.repo.delete(model.id)
            await self.repo.session.commit()

        except Exception as e:
            raise InternalServerError(
                f"Failed to delete record: {str(e)}", {"record_id": record_id}
            )

    async def approve(self, record_id: int, user_id: int) -> DailyRecord:
        """Approve the record for reporting."""
        try:
            model = await self.repo.get_record(record_id=record_id, user_id=user_id)
            entity = self.converter.convert(model, DailyRecord)

            entity.approve()

            updated_model = self.converter.convert(entity, DailyRecordModel)
            updated_model.id = model.id

            saved_model = await self.repo.update(updated_model)
            await self.repo.session.commit()
            return self.converter.convert(saved_model, DailyRecord)

        except Exception as e:
            raise InternalServerError(
                f"Failed to approve record: {str(e)}", {"record_id": record_id}
            )

    async def process_with_ai(self, record_id: int, user_id: int) -> DailyRecord:
        """Process record with AI."""
        try:
            model = await self.repo.get_record(record_id=record_id, user_id=user_id)

            entity = self.converter.convert(model, DailyRecord)

            if not self.ai_use_cases:
                raise InternalServerError("AI service not available")

            ai_result = await self.ai_use_cases.process_record(entity.raw_input, user_id)

            entity.mark_as_processed(ai_result)

            updated_model = self.converter.convert(entity, DailyRecordModel)
            updated_model.id = model.id

            saved_model = await self.repo.update(updated_model)
            await self.repo.session.commit()

            return self.converter.convert(saved_model, DailyRecord)

        except Exception as e:
            raise InternalServerError(
                f"Failed to process record with AI: {str(e)}",
                {"record_id": record_id, "user_id": user_id},
            )
