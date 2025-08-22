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
        """Create a new report."""
        result = await report_service.create_report(data)
        return SuccessResponse(message="Report created successfully", data=result)

    @get("/{report_id:int}", return_dto=DailyReportResponseDTO)
    @inject
    async def get_report(
        self, report_service: FromDishka[ReportService], report_id: int
    ) -> SuccessResponse:
        """Get a specific report."""
        result = await report_service.get_report(report_id)
        return SuccessResponse(message="Report retrieved successfully", data=result)

    @get(return_dto=DailyReportResponseDTO)
    @inject
    async def get_reports(
        self, report_service: FromDishka[ReportService], date: datetime | None = None
    ) -> SuccessResponse:
        """Get all reports."""
        result = await report_service.get_reports()
        return SuccessResponse(message="Reports retrieved successfully", data=result)

    @delete("/{report_id:int}", status_code=204)
    @inject
    async def delete_report(
        self, report_service: FromDishka[ReportService], report_id: int
    ) -> None:
        """Delete a report."""
        await report_service.delete_report(report_id)

    @patch("/{report_id:int}", return_dto=DailyReportResponseDTO)
    @inject
    async def update_report(
        self,
        report_service: FromDishka[ReportService],
        report_id: int,
    ) -> SuccessResponse:
        """Update a report."""
        update_data = DailyReportRequestUpdate(report_id=report_id)
        result = await report_service.update_report(update_data)
        return SuccessResponse(message="Report updated successfully", data=result)
