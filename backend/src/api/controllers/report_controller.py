from datetime import datetime

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, patch, post

from backend.src.api.dto import (
    DailyReportRequest,
    DailyReportRequestDTO,
    DailyReportRequestUpdate,
    DailyReportResponseDTO,
)
from backend.src.services import ReportService
from backend.src.api.responses.base_responses import SuccessResponse


class ReportController(Controller):
    @post(dto=DailyReportRequestDTO, return_dto=DailyReportResponseDTO)
    @inject
    async def create_report(
        self, data: DailyReportRequest, report_service: FromDishka[ReportService]
    ) -> SuccessResponse:
        result = await report_service.create_report(data)
        return SuccessResponse(message="Report created successfully", data=result)

    @get("/{report_id:int}", return_dto=DailyReportResponseDTO)
    @inject
    async def get_report(
        self, report_service: FromDishka[ReportService], report_id: int
    ) -> SuccessResponse:
        result = await report_service.get_report(report_id)
        return SuccessResponse(message="Report retrieved successfully", data=result)

    @get(return_dto=DailyReportResponseDTO)
    @inject
    async def get_reports(
        self, report_service: FromDishka[ReportService], date: datetime | None
    ) -> SuccessResponse:
        result = await report_service.get_reports()
        return SuccessResponse(message="Reports retrieved successfully", data=result)

    @delete("/{report_id:int}")
    @inject
    async def delete_report(
        self, report_service: FromDishka[ReportService], report_id: int
    ) -> SuccessResponse:
        await report_service.delete_report(report_id)
        return SuccessResponse(message="Report deleted successfully")

    @patch("/{report_id:int}", return_dto=DailyReportResponseDTO)
    @inject
    async def update_report(
        self,
        report_service: FromDishka[ReportService],
        update_data: DailyReportRequestUpdate,
    ) -> SuccessResponse:
        result = await report_service.update_report(update_data)
        return SuccessResponse(message="Report updated successfully", data=result)
