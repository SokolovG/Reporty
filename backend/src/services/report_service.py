from datetime import datetime
from logging import getLogger

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
    UserSettingsRepository,
)
from backend.src.services.report_data_provider import ReportDataProvider

logger = getLogger(__name__)


class ReportService:
    def __init__(
        self,
        report_repo: ReportRepository,
        record_repo: DailyRecordRepository,
        report_data_provider: ReportDataProvider,
        user_settings_repo: UserSettingsRepository,
    ) -> None:
        self.repo = report_repo
        self.record_repo = record_repo
        self.report_data_provider = report_data_provider
        self.user_settings_repo = user_settings_repo

    async def create_report(self, data: DailyReportRequest) -> DailyReportResponse:
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
        logger.info(f"today record - {today_records}")
        logger.info(f"open records record - {open_records}")
        logger.info(f"tasks - {unique_records}")

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

    async def get_report(self, report_id: int) -> DailyReportResponse:
        report = await self.repo.get(report_id)
        return DailyReportResponse(
            id=report.id,
            report_date=report.report_date,
            content=report.content,
            entries_count=report.entries_count,
            generated_at=report.generated_at,
        )

    async def delete_report(self, report_id: int) -> None:
        record = await self.repo.delete(report_id)  # noqa

    async def update_report(self, update_data: DailyReportRequestUpdate) -> None:
        pass

    def _format_records_to_text(self, records: list, report_date: datetime) -> str:
        date_str = report_date.strftime("%d.%m.%Y")

        lines = [f"Report for {date_str}", ""]

        for i, record in enumerate(records, 1):
            description = record.final_description or record.ai_processed or record.raw_input
            lines.append(f"{i}. {description}")

        lines.append(f"\nTotal tasks: {len(records)}")

        return "\n".join(lines)
