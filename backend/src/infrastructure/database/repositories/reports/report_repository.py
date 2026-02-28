from collections.abc import Sequence
from datetime import date

from advanced_alchemy import repository
from sqlalchemy import and_, select

from backend.src.application.dto.reports import ReportUpdateData
from backend.src.domain.entities.report import Report
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.models import ReportModel
from backend.src.infrastructure.exceptions.api_exceptions import NotFoundError


class ReportRepository(repository.SQLAlchemyAsyncRepository[ReportModel]):  # ty: ignore
    model_type: type[ReportModel] = ReportModel

    def __init__(self, converter: Converter, **kwargs) -> None:
        super().__init__(**kwargs)
        self.converter = converter

    async def get_latest_report(self, user_id: int) -> Report | None:
        """Get the most recent report."""
        result = await self.session.execute(
            select(ReportModel)
            .order_by(ReportModel.generated_at.desc())
            .limit(1)
            .where(ReportModel.user_id == user_id)
        )
        model = result.scalar_one_or_none()
        return self.converter.convert(model, Report)

    async def get_reports_by_date_range(
        self, start_date: date, end_date: date, user_id: int
    ) -> Sequence[Report]:
        """Get reports within date range."""
        result = await self.session.execute(
            select(ReportModel)
            .where(and_(ReportModel.report_date >= start_date, ReportModel.report_date <= end_date))
            .order_by(ReportModel.report_date.desc())
            .where(ReportModel.user_id == user_id)
        )
        models = result.scalars().all()
        return self.converter.convert_list(list(models), Report)

    async def update_report(self, update_data: ReportUpdateData, user_id: int) -> Report:
        report_model = await self.get_report_model(report_id=update_data.report_id, user_id=user_id)
        if update_data.content is not None:
            report_model.content = update_data.content
        updated_model = await self.update(report_model)
        await self.session.commit()
        await self.session.refresh(updated_model)
        return self.converter.convert(updated_model, Report)

    async def get_report(self, report_id: int, user_id: int) -> Report:
        report = await self.get_report_model(report_id, user_id)
        return self.converter.convert(report, Report)

    async def get_report_model(self, report_id: int, user_id: int) -> ReportModel:
        query = await self.session.execute(
            select(ReportModel)
            .where(ReportModel.id == report_id)
            .where(ReportModel.user_id == user_id)
        )
        report = query.scalar_one_or_none()
        if not report:
            raise NotFoundError("Report", report_id)
        return report

    async def create_report(self, report_entity: Report) -> Report:
        """Create a new report from entity."""
        model = ReportModel(
            report_date=report_entity.report_date,
            content=report_entity.content,
            entries_count=report_entity.entries_count,
            user_id=report_entity.user_id,
        )
        saved = await self.add(model)
        await self.session.commit()
        await self.session.refresh(saved)
        return self.converter.convert(saved, Report)

    async def list_reports(self, user_id: int | None = None) -> Sequence[Report]:
        """List all reports, optionally filtered by user."""
        stmt = select(ReportModel).order_by(ReportModel.generated_at.desc())
        if user_id is not None:
            stmt = stmt.where(ReportModel.user_id == user_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return self.converter.convert_list(list(models), Report)
