from collections.abc import Sequence
from datetime import date

from advanced_alchemy import repository
from sqlalchemy import and_, select

from backend.src.infrastructure.database.models import ReportModel
from backend.src.infrastructure.exceptions.api_exceptions import NotFoundError
from backend.src.presentation.dto import DailyReportRequestUpdate


class ReportRepository(repository.SQLAlchemyAsyncRepository[ReportModel]):  # ty: ignore
    model_type: type[ReportModel] = ReportModel

    async def get_latest_report(self, user_id: int) -> ReportModel | None:
        """Get the most recent report."""
        result = await self.session.execute(
            select(ReportModel)
            .order_by(ReportModel.generated_at.desc())
            .limit(1)
            .where(ReportModel.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_reports_by_date_range(
        self, start_date: date, end_date: date, user_id: int
    ) -> Sequence[ReportModel]:
        """Get reports within date range."""
        result = await self.session.execute(
            select(ReportModel)
            .where(and_(ReportModel.report_date >= start_date, ReportModel.report_date <= end_date))
            .order_by(ReportModel.report_date.desc())
            .where(ReportModel.user_id == user_id)
        )
        return result.scalars().all()

    async def update_report(
        self, update_data: DailyReportRequestUpdate, user_id: int
    ) -> ReportModel:
        report = await self.get_report(report_id=update_data.report_id, user_id=user_id)
        updated_report = await self.update(report)
        return updated_report

    async def get_report(self, report_id: int, user_id: int) -> ReportModel:
        query = await self.session.execute(
            select(ReportModel)
            .where(ReportModel.id == report_id)
            .where(ReportModel.user_id == user_id)
        )
        report = query.scalar_one_or_none()
        if not report:
            raise NotFoundError("Report", report_id)
        return report
