from collections.abc import Sequence
from datetime import date, datetime

from advanced_alchemy import repository
from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload

from backend.src.api.dto import DailyRecordRequest, RecordStatusUpdateRequest
from backend.src.database.base import RecordStatus
from backend.src.database.models import DailyRecord, ExternalTask


class DailyRecordRepository(repository.SQLAlchemyAsyncRepository[DailyRecord]):  # type: ignore
    model_type: type[DailyRecord] = DailyRecord

    async def create_record(self, data: DailyRecordRequest) -> DailyRecord:
        if data.external_task_id is not None:
            await self._validate_external_task_exists(data.external_task_id)

        record = DailyRecord(
            user_id=data.user_id,
            title=data.title,
            raw_input=data.raw_input,
            external_task_id=data.external_task_id,
            external_url=data.external_task_url,
        )

        added_record = await self.add(record)
        await self.session.commit()
        return added_record

    async def update_record_status(self, record_id: int, data: RecordStatusUpdateRequest) -> None:
        return None

    async def get_by_title_user_and_date(
        self, title: str, user_id: int, day: date
    ) -> DailyRecord | None:
        start = datetime.combine(day, datetime.min.time())
        end = datetime.combine(day, datetime.max.time())
        result = await self.session.execute(
            select(DailyRecord)
            .where(DailyRecord.user_id == user_id)
            .where(DailyRecord.title == title)
            .where(DailyRecord.created_at >= start)
            .where(DailyRecord.created_at <= end)
        )
        return result.scalar_one_or_none()

    async def get_with_external_task(self, record_id: int) -> DailyRecord:
        """Get record with loaded external task and system info."""
        result = await self.session.execute(
            select(DailyRecord)
            .options(selectinload(DailyRecord.external_task).selectinload(ExternalTask.system))
            .where(DailyRecord.id == record_id)
        )
        record = result.scalar_one()
        return record

    async def get_records_by_date(
        self, target_date: date, user_id: int | None = None, include_external_tasks: bool = False
    ) -> Sequence[DailyRecord]:
        """Get all records for a specific date."""
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())

        query = select(DailyRecord).where(
            and_(DailyRecord.created_at >= start_datetime, DailyRecord.created_at <= end_datetime)
        )

        if user_id is not None:
            query = query.where(DailyRecord.user_id == user_id)

        if include_external_tasks:
            query = query.options(
                selectinload(DailyRecord.external_task).selectinload(ExternalTask.system)
            )

        query = query.order_by(DailyRecord.created_at.asc())

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

    async def get_records_for_external_task(self, external_task_id: int) -> Sequence[DailyRecord]:
        """Get all records linked to a specific external task."""
        result = await self.session.execute(
            select(DailyRecord)
            .where(DailyRecord.external_task_id == external_task_id)
            .order_by(DailyRecord.created_at.desc())
        )
        return result.scalars().all()

    async def _validate_external_task_exists(self, external_task_id: int) -> None:
        """Validate that external task exists."""
        result = await self.session.execute(
            select(ExternalTask.id).where(ExternalTask.id == external_task_id)
        )
        if result.scalar_one_or_none() is None:
            raise ValueError(f"External task with id {external_task_id} not found")

    async def get_records_by_status(
        self, status: RecordStatus, user_id: int | None = None
    ) -> Sequence[DailyRecord]:
        """Get records by status."""
        query = select(DailyRecord).where(DailyRecord.status == status.value)

        if user_id is not None:
            query = query.where(DailyRecord.user_id == user_id)

        query = query.order_by(DailyRecord.created_at.desc())

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all_records(self, user_id: int | None = None) -> Sequence[DailyRecord]:
        query = select(DailyRecord)
        if user_id is not None:
            query = query.where(DailyRecord.user_id == user_id)

        query = query.order_by(DailyRecord.created_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all()
