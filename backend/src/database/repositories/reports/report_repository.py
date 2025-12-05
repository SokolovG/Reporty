from collections.abc import Sequence
from datetime import date

from advanced_alchemy import repository
from sqlalchemy import and_, select

from backend.src.api.dto.reports.requests import DailyReportRequestUpdate
from backend.src.core.exceptions import NotFoundError
from backend.src.database.models import Report


class ReportRepository(repository.SQLAlchemyAsyncRepository[Report]):  # type: ignore
    model_type: type[Report] = Report

    async def get_latest_report(self, user_id: int) -> Report | None:
        """Get the most recent report."""
        result = await self.session.execute(
            select(Report)
            .order_by(Report.generated_at.desc())
            .limit(1)
            .where(Report.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_reports_by_date_range(
        self, start_date: date, end_date: date, user_id: int
    ) -> Sequence[Report]:
        """Get reports within date range."""
        result = await self.session.execute(
            select(Report)
            .where(and_(Report.report_date >= start_date, Report.report_date <= end_date))
            .order_by(Report.report_date.desc())
            .where(Report.user_id == user_id)
        )
        return result.scalars().all()

    async def update_report(self, update_data: DailyReportRequestUpdate, user_id: int) -> Report:
        report = await self.get_report(report_id=update_data.report_id, user_id=user_id)
        updated_report = await self.update(report)
        return updated_report

    async def get_report(self, report_id: int, user_id: int) -> Report:
        query = await self.session.execute(
            select(Report).where(Report.id == report_id).where(Report.user_id == user_id)
        )
        report = query.scalar_one_or_none()
        if not report:
            raise NotFoundError("Report", report_id)
        return report
