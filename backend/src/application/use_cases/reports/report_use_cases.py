from datetime import datetime
from logging import getLogger

from backend.src.infrastructure.database.base import RecordStatus
from backend.src.infrastructure.database.models import DailyRecordModel, ReportModel
from backend.src.infrastructure.database.repositories import (
    DailyRecordRepository,
    ReportRepository,
    UserRepository,
)
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError, NotFoundError
from backend.src.presentation.dto import (
    DailyReportRequest,
    DailyReportRequestUpdate,
)

logger = getLogger(__name__)


class ReportUseCases:
    def __init__(
        self,
        report_repo: ReportRepository,
        record_repo: DailyRecordRepository,
        user_repository: UserRepository,
    ) -> None:
        self.repo = report_repo
        self.record_repo = record_repo
        self.user_repository = user_repository

    async def create(self, data: DailyReportRequest, user_id: int) -> ReportModel:
        """Create a new daily report."""
        try:
            today_records = await self.record_repo.get_records_by_date(
                target_date=data.date, user_id=user_id
            )
            open_records = await self.record_repo.get_records_by_status(
                status=RecordStatus.OPEN, user_id=user_id
            )

            # TODO: make better SQL, not N+1

            set_ids = set()
            unique_records = []
            for record in list(open_records) + list(today_records):
                if record.id not in set_ids:
                    set_ids.add(record.id)
                    unique_records.append(record)

            report_content = self._format_records_to_text(unique_records, data.date)

            report = await self.repo.add(
                ReportModel(
                    report_date=data.date,
                    content=report_content,
                    entries_count=len(unique_records),
                    user_id=user_id,
                )
            )
            await self.repo.session.commit()

            return report
        except Exception as e:
            raise InternalServerError(f"Failed to create report: {str(e)}", {"user_id": user_id})

    async def get(self, report_id: int, user_id: int) -> ReportModel:
        """Get a specific report by ID."""
        try:
            report = await self.repo.get_report(report_id=report_id, user_id=user_id)
            return report
        except Exception as e:
            raise InternalServerError(f"Failed to get report: {str(e)}", {"report_id": report_id})

    async def delete(self, report_id: int, user_id: int) -> None:
        """Delete a report."""
        try:
            report = await self.repo.get_report(report_id=report_id, user_id=user_id)
            await self.repo.delete(report.id)
            await self.repo.session.commit()
        except NotFoundError:
            raise
        except Exception as e:
            raise InternalServerError(
                f"Failed to delete report: {str(e)}", {"report_id": report_id}
            )

    async def update(self, update_data: DailyReportRequestUpdate, user_id: int) -> ReportModel:
        """Update a report."""
        try:
            report = await self.repo.get_report(report_id=update_data.report_id, user_id=user_id)
            # TODO: Implement actual update logic
            updated_report = await self.repo.update(report)
            await self.repo.session.commit()

            return updated_report
        except Exception as e:
            raise InternalServerError(
                f"Failed to update report: {str(e)}", {"report_id": update_data.report_id}
            )

    async def get_many(self, user_id: int) -> list[ReportModel]:
        """Get all reports."""
        try:
            reports = await self.repo.list(user_id=user_id)

            if not reports:
                raise NotFoundError("Report")

            return list(reports)
        except Exception as e:
            raise InternalServerError(f"Failed to get reports: {str(e)}")

    def _format_records_to_text(
        self, records: list[DailyRecordModel], report_date: datetime
    ) -> str:
        """Format records into a readable text report."""
        date_str = report_date.strftime("%d.%m.%Y")

        lines = [f"Report for {date_str}", ""]

        for i, record in enumerate(records, 1):
            description = record.final_description or record.ai_processed or record.raw_input
            lines.append(f"{i}. {description}")

        lines.append(f"\nTotal tasks: {len(records)}")

        return "\n".join(lines)
