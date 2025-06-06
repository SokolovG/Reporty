from backend.src.api.dto import (
    DailyReportRequest,
    DailyReportRequestUpdate,
    DailyReportResponse,
)
from backend.src.database.repositories import DailyReportRepository


class ReportService:
    def __init__(self, report_repo: DailyReportRepository) -> None:
        self.repo = report_repo

    async def create_report(self, data: DailyReportRequest) -> DailyReportResponse:
        saved_record = await self.repo.create_report(data)  # noqa
        return DailyReportResponse()

    async def get_report(self, report_id: int) -> DailyReportResponse:
        record = await self.repo.get(report_id)  # noqa
        return DailyReportResponse()

    async def delete_report(self, report_id: int) -> DailyReportResponse:
        record = await self.repo.delete(report_id)  # noqa
        return DailyReportResponse()

    async def update_report(
        self, update_data: DailyReportRequestUpdate
    ) -> DailyReportResponse:
        record = await self.repo.update_report(update_data)  # noqa
        return DailyReportResponse()
