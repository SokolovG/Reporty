from collections.abc import Sequence
from datetime import date

from advanced_alchemy import repository
from sqlalchemy import and_, select

from backend.src.api.dto.report_dto import DailyReportRequest, DailyReportRequestUpdate
from backend.src.database.models import Report


class DailyReportRepository(repository.SQLAlchemyAsyncRepository[Report]):  # type: ignore
    model_type: type[Report] = Report

    async def create_report(self, dto: DailyReportRequest) -> Report:
        record = Report()
        return await self.add(record)

    async def get_latest_report(self) -> Report | None:
        """Get the most recent report."""
        result = await self.session.execute(
            select(Report).order_by(Report.generated_at.desc()).limit(1)
        )
        return result.scalar_one_or_none()

    async def get_reports_by_date_range(self, start_date: date, end_date: date) -> Sequence[Report]:
        """Get reports within date range."""
        result = await self.session.execute(
            select(Report)
            .where(and_(Report.report_date >= start_date, Report.report_date <= end_date))
            .order_by(Report.report_date.desc())
        )
        return result.scalars().all()

    async def update_report(self, update_data: DailyReportRequestUpdate) -> Report:
        report = await self.get(DailyReportRequestUpdate.report_id)
        return await self.update(report)
