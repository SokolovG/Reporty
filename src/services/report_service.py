from src.api.dto import DailyReportResponse


class ReportService:
    async def generate_report(self, date: str) -> DailyReportResponse:  # type: ignore
        pass

    async def get_report(self, date: str) -> DailyReportResponse:  # type: ignore
        pass
