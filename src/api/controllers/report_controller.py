from litestar import Controller, get, post

from src.api.dto import (
    DailyReportRequest,
    DailyReportRequestDTO,
    DailyReportResponse,
    DailyReportResponseDTO,
)
from src.services import ReportService


class ReportController(Controller):
    @post(dto=DailyReportRequestDTO, return_dto=DailyReportResponseDTO)
    async def create_report(
        self, data: DailyReportRequest, report_service: ReportService
    ) -> DailyReportResponse:
        return await report_service.create_report(data)

    @get("/{record_id:uuid}", return_dto=DailyReportResponseDTO)
    async def get_report(
        self, report_service: ReportService, report_id: int
    ) -> DailyReportResponse:
        return await report_service.get_report(report_id)
