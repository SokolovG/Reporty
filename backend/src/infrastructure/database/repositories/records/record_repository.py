from collections.abc import Sequence
from datetime import date, datetime

from advanced_alchemy import repository
from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload

from backend.src.application.dto.records import DailyRecordData
from backend.src.domain.entities.record import DailyRecord
from backend.src.domain.value_objects import RecordStatus
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.models import (
    DailyRecordModel,
    ExternalTaskModel,
)
from backend.src.infrastructure.exceptions.api_exceptions import NotFoundError


class DailyRecordRepository(
    repository.SQLAlchemyAsyncRepository[DailyRecordModel]  # ty:ignore[invalid-type-arguments]
):
    model_type: type[DailyRecordModel] = DailyRecordModel

    def __init__(self, converter: Converter, **kwargs) -> None:
        super().__init__(**kwargs)
        self.converter = converter

    async def create_record(self, data: DailyRecordData, user_id: int) -> DailyRecord:
        if data.external_task_id is not None:
            await self._validate_external_task_exists(data.external_task_id)

        record = DailyRecordModel(
            user_id=user_id,
            title=data.title,
            raw_input=data.raw_input,
            external_task_id=data.external_task_id,
            external_url=data.external_task_url,
        )

        added_record = await self.add(record)
        await self.session.commit()
        await self.session.refresh(added_record)
        return self.converter.convert(added_record, DailyRecord)

    async def get_record(self, record_id: int, user_id: int) -> DailyRecord:
        query = await self.session.execute(
            select(DailyRecordModel)
            .where(DailyRecordModel.id == record_id)
            .where(DailyRecordModel.user_id == user_id)
        )

        record = query.scalar_one_or_none()
        if not record:
            raise NotFoundError("Daily record", record_id)
        return self.converter.convert(record, DailyRecord)

    async def get_by_title_user_and_date(
        self, title: str, user_id: int, day: date
    ) -> DailyRecord | None:
        start = datetime.combine(day, datetime.min.time())
        end = datetime.combine(day, datetime.max.time())
        result = await self.session.execute(
            select(DailyRecordModel)
            .where(DailyRecordModel.user_id == user_id)
            .where(DailyRecordModel.title == title)
            .where(DailyRecordModel.created_at >= start)
            .where(DailyRecordModel.created_at <= end)
        )
        model = result.scalar_one_or_none()
        return self.converter.convert(model, DailyRecord) if model else None

    async def get_with_external_task(self, record_id: int, user_id: int) -> DailyRecord:
        """Get record with loaded external task and system info."""
        result = await self.session.execute(
            select(DailyRecordModel)
            .options(
                selectinload(DailyRecordModel.external_task).selectinload(ExternalTaskModel.system)
            )
            .where(DailyRecordModel.id == record_id)
            .where(DailyRecordModel.user_id == user_id)
        )
        record = result.scalar_one_or_none()
        if not record:
            raise NotFoundError(f"Record {record_id} not found for user {user_id}")
        return self.converter.convert(record, DailyRecord)

    async def get_records_by_date(
        self, target_date: date, user_id: int, include_external_tasks: bool = False
    ) -> Sequence[DailyRecord]:
        """Get all records for a specific date."""
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())

        query = select(DailyRecordModel).where(
            and_(
                DailyRecordModel.created_at >= start_datetime,
                DailyRecordModel.created_at <= end_datetime,
            )
        )

        if include_external_tasks:
            query = query.options(
                selectinload(DailyRecordModel.external_task).selectinload(ExternalTaskModel.system)
            )

        query = query.order_by(DailyRecordModel.created_at.asc()).where(
            DailyRecordModel.user_id == user_id
        )

        result = await self.session.execute(query)
        models = result.scalars().all()
        return self.converter.convert_list(list(models), DailyRecord)

    async def get_unprocessed_records(self, user_id: int) -> Sequence[DailyRecord]:
        """Get records that haven't been processed by AI yet."""
        result = await self.session.execute(
            select(DailyRecordModel)
            .where(DailyRecordModel.is_processed == False)  # noqa: E712
            .order_by(DailyRecordModel.created_at.asc())
            .where(DailyRecordModel.user_id == user_id)
        )
        models = result.scalars().all()
        return self.converter.convert_list(list(models), DailyRecord)

    async def get_records_for_external_task(
        self, external_task_id: int, user_id: int
    ) -> Sequence[DailyRecord]:
        """Get all records linked to a specific external task."""
        result = await self.session.execute(
            select(DailyRecordModel)
            .where(DailyRecordModel.external_task_id == external_task_id)
            .order_by(DailyRecordModel.created_at.desc())
            .where(DailyRecordModel.user_id == user_id)
        )
        models = result.scalars().all()
        return self.converter.convert_list(list(models), DailyRecord)

    async def _validate_external_task_exists(self, external_task_id: int) -> None:
        """Validate that external task exists."""
        result = await self.session.execute(
            select(ExternalTaskModel.id).where(ExternalTaskModel.id == external_task_id)
        )
        if result.scalar_one_or_none() is None:
            raise ValueError(f"External task with id {external_task_id} not found")

    async def get_records_by_status(
        self, status: RecordStatus, user_id: int
    ) -> Sequence[DailyRecord]:
        """Get records by status."""
        query = (
            select(DailyRecordModel)
            .where(DailyRecordModel.status == status.value)
            .order_by(DailyRecordModel.created_at.desc())
            .where(DailyRecordModel.user_id == user_id)
        )
        result = await self.session.execute(query)
        models = result.scalars().all()
        return self.converter.convert_list(list(models), DailyRecord)

    async def get_all_records(self, user_id: int) -> Sequence[DailyRecord]:
        query = (
            select(DailyRecordModel)
            .order_by(DailyRecordModel.created_at.desc())
            .where(DailyRecordModel.user_id == user_id)
        )
        result = await self.session.execute(query)
        models = result.scalars().all()
        return self.converter.convert_list(list(models), DailyRecord)

    async def update_record(self, entity: DailyRecord) -> DailyRecord:
        """Update record from entity."""
        model = await self.get(entity.id)

        model.title = entity.title
        model.raw_input = entity.raw_input
        model.ai_processed = entity.ai_processed
        model.is_processed = entity.is_processed
        model.processed_at = entity.processed_at
        model.is_approved = entity.is_approved
        model.final_description = entity.final_description
        model.external_task_id = entity.external_task_id
        model.external_url = entity.external_url
        model.status = entity.status

        await self.session.commit()
        await self.session.refresh(model)
        return self.converter.convert(model, DailyRecord)

    async def delete_record(self, record_id: int) -> None:
        """Delete record and commit."""
        model = await self.get(record_id)
        await self.session.delete(model)
        await self.session.commit()
