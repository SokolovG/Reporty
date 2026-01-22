from datetime import datetime

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, Request, delete, get, patch, post

from backend.src.application.dto.reports import ReportData, ReportUpdateData
from backend.src.application.use_cases.reports.report_use_cases import ReportUseCases
from backend.src.infrastructure.database.mappers import Converter
from backend.src.presentation.dto.reports import (
    ReportRequestDTO,
    ReportResponse,
)
from backend.src.presentation.responses.base_responses import SuccessResponse, SuccessResponseDTO


class ReportController(Controller):
    @post(dto=ReportRequestDTO, return_dto=SuccessResponseDTO)
    @inject
    async def create_report(
        self,
        request: Request,
        data: ReportData,
        report_use_cases: FromDishka[ReportUseCases],
        converter: FromDishka[Converter],
    ) -> SuccessResponse:
        """Create a new report."""
        user_id = request.user.id
        report = await report_use_cases.create(data=data, user_id=user_id)
        result = converter.convert(report, ReportResponse)
        return SuccessResponse(message="Report created successfully", data=result)

    @get("/{report_id:int}", return_dto=SuccessResponseDTO)
    @inject
    async def get_report(
        self,
        request: Request,
        report_id: int,
        report_use_cases: FromDishka[ReportUseCases],
        converter: FromDishka[Converter],
    ) -> SuccessResponse:
        """Get a specific report."""
        user_id = request.user.id
        report = await report_use_cases.get(report_id=report_id, user_id=user_id)
        result = converter.convert(report, ReportResponse)
        return SuccessResponse(message="Report retrieved successfully", data=result)

    @get(return_dto=SuccessResponseDTO)
    @inject
    async def get_reports(
        self,
        request: Request,
        report_use_cases: FromDishka[ReportUseCases],
        converter: FromDishka[Converter],
        date: datetime | None = None,
    ) -> SuccessResponse:
        """Get all reports."""
        user_id = request.user.id
        reports = await report_use_cases.get_many(user_id=user_id)
        result = [converter.convert(report, ReportResponse) for report in reports]
        return SuccessResponse(message="Reports retrieved successfully", data=result)

    @delete("/{report_id:int}", status_code=204)
    @inject
    async def delete_report(
        self,
        request: Request,
        report_id: int,
        report_use_cases: FromDishka[ReportUseCases],
    ) -> None:
        """Delete a report."""
        user_id = request.user.id
        await report_use_cases.delete(report_id=report_id, user_id=user_id)

    @patch("/{report_id:int}", return_dto=SuccessResponseDTO)
    @inject
    async def update_report(
        self,
        request: Request,
        update_data: ReportUpdateData,
        report_use_cases: FromDishka[ReportUseCases],
        converter: FromDishka[Converter],
    ) -> SuccessResponse:
        """Update a report."""
        user_id = request.user.id
        report = await report_use_cases.update(update_data=update_data, user_id=user_id)
        result = converter.convert(report, ReportResponse)
        return SuccessResponse(message="Report updated successfully", data=result)
