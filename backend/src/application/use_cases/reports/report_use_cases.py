from collections.abc import Sequence
from datetime import datetime
from logging import getLogger

from backend.src.application.dto.reports import ReportData, ReportUpdateData
from backend.src.application.ports.repositories import (
    IDailyRecordRepository,
    IReportRepository,
    IUserRepository,
)
from backend.src.domain.entities.record import DailyRecord
from backend.src.domain.entities.report import Report
from backend.src.domain.exceptions.domain_exceptions import (
    NoRecordsForReportError,
    ReportGenerationError,
)
from backend.src.domain.value_objects import RecordStatus
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError, NotFoundError

logger = getLogger(__name__)


class ReportUseCases:
    def __init__(
        self,
        report_repo: IReportRepository,
        record_repo: IDailyRecordRepository,
        user_repository: IUserRepository,
        converter: Converter,
    ) -> None:
        self.repo = report_repo
        self.record_repo = record_repo
        self.user_repository = user_repository
        self.converter = converter

    async def create(self, data: ReportData, user_id: int) -> Report:
        """Create a new daily report."""
        try:
            today_records_models = await self.record_repo.get_records_by_date(
                target_date=data.date, user_id=user_id
            )
            open_records_models = await self.record_repo.get_records_by_status(
                status=RecordStatus.OPEN, user_id=user_id
            )

            set_ids = set()
            unique_records_models = []
            for record in list(open_records_models) + list(today_records_models):
                if record.id not in set_ids:
                    set_ids.add(record.id)
                    unique_records_models.append(record)

            report_content = self._format_records_to_text(unique_records_models, data.date)

            report_entity = Report.create(
                user_id=user_id,
                report_date=data.date,
                content=report_content,
                entries_count=len(unique_records_models),
            )

            saved_report = await self.repo.create_report(report_entity)
            return saved_report

        except Exception as e:
            if isinstance(e, (NoRecordsForReportError, ReportGenerationError)):
                raise e
            raise InternalServerError(f"Failed to create report: {str(e)}", {"user_id": user_id})

    async def get(self, report_id: int, user_id: int) -> Report:
        """Get a specific report by ID."""
        try:
            return await self.repo.get_report(report_id=report_id, user_id=user_id)

        except Exception as e:
            raise InternalServerError(f"Failed to get report: {str(e)}", {"report_id": report_id})

    async def delete(self, report_id: int, user_id: int) -> None:
        """Delete a report."""
        try:
            await self.repo.delete(report_id)
            await self.repo.session.commit()
        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(
                f"Failed to delete report: {str(e)}", {"report_id": report_id}
            )

    async def update(self, update_data: ReportUpdateData, user_id: int) -> Report:
        """Update a report content."""
        try:
            updated_report = await self.repo.update_report(update_data, user_id)
            return updated_report

        except Exception as e:
            if isinstance(e, NotFoundError):
                raise e
            raise InternalServerError(
                f"Failed to update report: {str(e)}", {"report_id": update_data.report_id}
            )

    async def get_many(self, user_id: int) -> Sequence[Report]:
        """Get all reports."""
        try:
            return await self.repo.list_reports(user_id=user_id)

        except Exception as e:
            raise InternalServerError(f"Failed to get reports: {str(e)}")

    def _format_records_to_text(self, records: Sequence[DailyRecord], report_date: datetime) -> str:
        """Format records into a readable text report."""
        date_str = report_date.strftime("%d.%m.%Y")

        lines = [f"Report for {date_str}", ""]

        for i, record in enumerate(records, 1):
            description = record.final_description or record.ai_processed or record.raw_input
            lines.append(f"{i}. {description}")

        lines.append(f"\nTotal tasks: {len(records)}")

        return "\n".join(lines)
