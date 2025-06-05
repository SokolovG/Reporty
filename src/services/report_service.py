from src.api.dto import DailyReportRequest, DailyReportResponse
from src.database.repositories import DailyReportRepository


class ReportService:
    def __init__(self, record_repo: DailyReportRepository) -> None:
        self.repo = record_repo

    async def create_report(self, data: DailyReportRequest) -> DailyReportResponse:
        saved_record = await self.repo.create_report(data)  # noqa
        return DailyReportResponse()

    async def get_report(self, report_id: int) -> DailyReportResponse:
        record = await self.repo.get(report_id)  # noqa
        return DailyReportResponse()
