from collections.abc import Sequence
from datetime import date
from uuid import UUID

from advanced_alchemy import repository
from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload

from src.api.dto import DailyRecordRequest
from src.database.models import DailyRecord, ExternalTask


class DailyRecordRepository(repository.SQLAlchemyAsyncRepository[DailyRecord]):  # type: ignore
    model_type: type[DailyRecord] = DailyRecord

    async def create_record(self, dto: DailyRecordRequest) -> DailyRecord:
        # Валидация external_task_id если указан
        if dto.external_task_id is not None:
            await self._validate_external_task_exists(dto.external_task_id)

        record = DailyRecord(
            raw_input=dto.raw_input,
            external_task_id=dto.external_task_id,
        )

        return await self.add(record)

    async def get_with_external_task(self, record_id: UUID) -> DailyRecord:
        """Get record with loaded external task and system info."""
        result = await self.session.execute(
            select(DailyRecord)
            .options(selectinload(DailyRecord.external_task).selectinload(ExternalTask.system))
            .where(DailyRecord.id == record_id)
        )
        record = result.scalar_one()
        return record

    async def get_records_by_date_range(
        self, start_date: date, end_date: date, include_external_tasks: bool = False
    ) -> Sequence[DailyRecord]:
        """Get records within date range, optionally with external task info."""
        query = (
            select(DailyRecord)
            .where(
                and_(
                    DailyRecord.created_at >= start_date,
                    DailyRecord.created_at <= end_date,
                )
            )
            .order_by(DailyRecord.created_at.desc())
        )

        if include_external_tasks:
            query = query.options(
                selectinload(DailyRecord.external_task).selectinload(ExternalTask.system)
            )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_unprocessed_records(self) -> Sequence[DailyRecord]:
        """Get records that haven't been processed by AI yet."""
        result = await self.session.execute(
            select(DailyRecord)
            .where(DailyRecord.is_processed == False)  # noqa: E712
            .order_by(DailyRecord.created_at.asc())
        )
        return result.scalars().all()

    async def get_records_for_external_task(self, external_task_id: UUID) -> Sequence[DailyRecord]:
        """Get all records linked to a specific external task."""
        result = await self.session.execute(
            select(DailyRecord)
            .where(DailyRecord.external_task_id == external_task_id)
            .order_by(DailyRecord.created_at.desc())
        )
        return result.scalars().all()

    async def _validate_external_task_exists(self, external_task_id: UUID) -> None:
        """Validate that external task exists."""
        result = await self.session.execute(
            select(ExternalTask.id).where(ExternalTask.id == external_task_id)
        )
        if result.scalar_one_or_none() is None:
            raise ValueError(f"External task with id {external_task_id} not found")
