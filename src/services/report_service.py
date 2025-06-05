from uuid import UUID

from src.api.dto import DailyRecordRequest, DailyReportResponse
from src.database.repositories import DailyRecordRepository


class ReportService:
    def __init__(self, record_repo: DailyRecordRepository) -> None:
        self.repo = record_repo

    async def create_report(self, data: DailyRecordRequest) -> DailyReportResponse:
        saved_record = await self.repo.create_record(data)
        return DailyReportResponse()

    async def get_report(self, report_id: UUID) -> DailyReportResponse:
        record = await self.repo.get(report_id)
        return DailyReportResponse()
