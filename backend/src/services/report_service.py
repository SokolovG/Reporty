from logging import getLogger

from backend.src.api.dto import (
    DailyReportRequest,
    DailyReportRequestUpdate,
    DailyReportResponse,
)
from backend.src.database.base import RecordStatus
from backend.src.database.repositories import DailyReportRepository, DailyRecordRepository


logger = getLogger(__name__)


class ReportService:
    def __init__(
        self, report_repo: DailyReportRepository, record_repo: DailyRecordRepository
    ) -> None:
        self.repo = report_repo
        self.record_repo = record_repo

    async def create_report(self, data: DailyReportRequest) -> DailyReportResponse:
        today_records = await self.record_repo.get_records_by_date(
            target_date=data.date, user_id=data.user_id
        )
        open_records = await self.record_repo.get_records_by_status(
            status=RecordStatus.OPEN, user_id=data.user_id
        )

        tasks = [today_records, open_records]

        logger.info(f"today record - {today_records}")
        logger.info(f"open records record - {open_records}")
        await self.repo.create_report(tasks)
        return DailyReportResponse()

    async def get_report(self, report_id: int) -> DailyReportResponse:
        record = await self.repo.get(report_id)  # noqa
        return DailyReportResponse()

    async def delete_report(self, report_id: int) -> None:
        record = await self.repo.delete(report_id)  # noqa

    async def update_report(self, update_data: DailyReportRequestUpdate) -> DailyReportResponse:
        record = await self.repo.update_report(update_data)  # noqa
        return DailyReportResponse()
