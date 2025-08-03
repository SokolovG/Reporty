from datetime import datetime

from dishka import FromDishka
from dishka.integrations.litestar import inject
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
    @inject
    async def create_report(
        self, data: DailyReportRequest, report_service: FromDishka[ReportService]
    ) -> DailyReportResponse:
        return await report_service.create_report(data)

    @get("/{report_id:int}", return_dto=DailyReportResponseDTO)
    @inject
    async def get_report(
        self, report_service: FromDishka[ReportService], report_id: int
    ) -> DailyReportResponse:
        return await report_service.get_report(report_id)

    @get(return_dto=DailyReportResponseDTO)
    @inject
    async def get_reports(
        self, report_service: FromDishka[ReportService], date: datetime | None
    ) -> list[DailyReportResponse]:
        return await report_service.get_reports()

    @delete("/{report_id:int}")
    @inject
    async def delete_report(
        self, report_service: FromDishka[ReportService], report_id: int
    ) -> None:
        await report_service.delete_report(report_id)

    @patch("/{report_id:int}", return_dto=DailyReportResponseDTO)
    @inject
    async def update_report(
        self,
        report_service: FromDishka[ReportService],
        update_data: DailyReportRequestUpdate,
    ) -> None:
        return await report_service.update_report(update_data)
