from litestar import Controller, delete, get, patch, post

from backend.src.api.dto import (
    DailyReportRequest,
    DailyReportRequestDTO,
    DailyReportRequestUpdate,
    DailyReportResponse,
    DailyReportResponseDTO,
)
from backend.src.services import ReportService


class ReportController(Controller):
    @post(dto=DailyReportRequestDTO, return_dto=DailyReportResponseDTO)
    async def create_report(
        self, data: DailyReportRequest, report_service: ReportService
    ) -> DailyReportResponse:
        return await report_service.create_report(data)

    @get("/{report_id:int}", return_dto=DailyReportResponseDTO)
    async def get_report(
        self, report_service: ReportService, report_id: int
    ) -> DailyReportResponse:
        return await report_service.get_report(report_id)

    @delete("/{report_id:int}")
    async def delete_report(self, report_service: ReportService, report_id: int) -> None:
        await report_service.delete_report(report_id)

    @patch("/{report_id:int}", return_dto=DailyReportResponseDTO)
    async def update_report(
        self, report_service: ReportService, update_data: DailyReportRequestUpdate
    ) -> DailyReportResponse:
        return await report_service.update_report(update_data)
