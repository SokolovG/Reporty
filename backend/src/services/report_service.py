from datetime import datetime
from logging import getLogger

from backend.src.core.exceptions import NotFoundError, InternalServerError
from backend.src.api.dto import (
    DailyReportRequest,
    DailyReportRequestUpdate,
    DailyReportResponse,
)
from backend.src.database.base import RecordStatus
from backend.src.database.models import Report
from backend.src.database.repositories import (
    ReportRepository,
    DailyRecordRepository,
    UserProfileRepository,
)

logger = getLogger(__name__)


class ReportService:
    def __init__(
        self,
        report_repo: ReportRepository,
        record_repo: DailyRecordRepository,
        user_profile_settings: UserProfileRepository,
    ) -> None:
        self.repo = report_repo
        self.record_repo = record_repo
        self.user_profile_settings = user_profile_settings

    async def create_report(self, data: DailyReportRequest) -> DailyReportResponse:
        """Create a new daily report."""
        try:
            today_records = await self.record_repo.get_records_by_date(
                target_date=data.date, user_id=data.user_id
            )
            open_records = await self.record_repo.get_records_by_status(
                status=RecordStatus.OPEN, user_id=data.user_id
            )

            set_ids = set()
            unique_records = []
            for record in list(open_records) + list(today_records):
                if record.id not in set_ids:
                    set_ids.add(record.id)
                    unique_records.append(record)

            logger.info(f"Today records: {len(today_records)}")
            logger.info(f"Open records: {len(open_records)}")
            logger.info(f"Unique records: {len(unique_records)}")

            report_content = self._format_records_to_text(unique_records, data.date)

            report = await self.repo.add(
                Report(
                    report_date=data.date,
                    content=report_content,
                    entries_count=len(unique_records),
                )
            )
            await self.repo.session.commit()

            return DailyReportResponse(
                id=report.id,
                report_date=report.report_date,
                content=report.content,
                entries_count=report.entries_count,
                generated_at=report.generated_at,
            )
        except Exception as e:
            raise InternalServerError(
                f"Failed to create report: {str(e)}", {"user_id": data.user_id}
            )

    async def get_report(self, report_id: int) -> DailyReportResponse:
        """Get a specific report by ID."""
        try:
            report = await self.repo.get(report_id)
            return DailyReportResponse(
                id=report.id,
                report_date=report.report_date,
                content=report.content,
                entries_count=report.entries_count,
                generated_at=report.generated_at,
            )
        except Exception as e:
            if "not found" in str(e).lower() or "No row was found" in str(e):
                raise NotFoundError("Report", report_id)
            raise InternalServerError(f"Failed to get report: {str(e)}", {"report_id": report_id})

    async def delete_report(self, report_id: int) -> None:
        """Delete a report."""
        try:
            await self.repo.delete(report_id)
        except Exception as e:
            if "not found" in str(e).lower() or "No row was found" in str(e):
                raise NotFoundError("Report", report_id)
            raise InternalServerError(
                f"Failed to delete report: {str(e)}", {"report_id": report_id}
            )

    async def update_report(self, update_data: DailyReportRequestUpdate) -> DailyReportResponse:
        """Update a report."""
        try:
            report = await self.repo.get(update_data.report_id)
            # TODO: Implement actual update logic
            updated_report = await self.repo.update(report)
            await self.repo.session.commit()

            return DailyReportResponse(
                id=updated_report.id,
                report_date=updated_report.report_date,
                content=updated_report.content,
                entries_count=updated_report.entries_count,
                generated_at=updated_report.generated_at,
            )
        except Exception as e:
            if "not found" in str(e).lower() or "No row was found" in str(e):
                raise NotFoundError("Report", update_data.report_id)
            raise InternalServerError(
                f"Failed to update report: {str(e)}", {"report_id": update_data.report_id}
            )

    async def get_reports(self) -> list[DailyReportResponse]:
        """Get all reports."""
        try:
            reports = await self.repo.list()
            response_list = []
            for report in reports:
                rep = DailyReportResponse(
                    id=report.id,
                    report_date=report.report_date,
                    content=report.content,
                    entries_count=report.entries_count,
                    generated_at=report.generated_at,
                )
                response_list.append(rep)
            return response_list
        except Exception as e:
            raise InternalServerError(f"Failed to get reports: {str(e)}")

    def _format_records_to_text(self, records: list, report_date: datetime) -> str:
        """Format records into a readable text report."""
        date_str = report_date.strftime("%d.%m.%Y")

        lines = [f"Report for {date_str}", ""]

        for i, record in enumerate(records, 1):
            description = record.final_description or record.ai_processed or record.raw_input
            lines.append(f"{i}. {description}")

        lines.append(f"\nTotal tasks: {len(records)}")

        return "\n".join(lines)
