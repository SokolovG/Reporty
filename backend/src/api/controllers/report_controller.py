from datetime import datetime

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, patch, post, Request

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
        self, data: DailyReportRequest, report_service: FromDishka[ReportService], request: Request
    ) -> SuccessResponse:
        """Create a new report."""
        user_id = request.user.id
        result = await report_service.create_report(data=data, user_id=user_id)
        return SuccessResponse(message="Report created successfully", data=result)

    @get("/{report_id:int}", return_dto=DailyReportResponseDTO)
    @inject
    async def get_report(
        self, report_service: FromDishka[ReportService], report_id: int, request: Request
    ) -> SuccessResponse:
        """Get a specific report."""
        user_id = request.user.id
        result = await report_service.get_report(report_id=report_id, user_id=user_id)
        return SuccessResponse(message="Report retrieved successfully", data=result)

    @get(return_dto=DailyReportResponseDTO)
    @inject
    async def get_reports(
        self,
        report_service: FromDishka[ReportService],
        request: Request,
        date: datetime | None = None,
    ) -> SuccessResponse:
        """Get all reports."""
        user_id = request.user.id
        result = await report_service.get_reports(user_id=user_id)
        return SuccessResponse(message="Reports retrieved successfully", data=result)

    @delete("/{report_id:int}", status_code=204)
    @inject
    async def delete_report(
        self, report_service: FromDishka[ReportService], report_id: int, request: Request
    ) -> None:
        """Delete a report."""
        user_id = request.user.id
        await report_service.delete_report(report_id=report_id, user_id=user_id)

    @patch("/{report_id:int}", return_dto=DailyReportResponseDTO)
    @inject
    async def update_report(
        self, report_service: FromDishka[ReportService], report_id: int, request: Request
    ) -> SuccessResponse:
        """Update a report."""
        user_id = request.user.id
        update_data = DailyReportRequestUpdate(report_id=report_id, user_id=user_id)
        result = await report_service.update_report(update_data=update_data, user_id=user_id)
        return SuccessResponse(message="Report updated successfully", data=result)
