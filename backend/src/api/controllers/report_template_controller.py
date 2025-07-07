from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get, post, patch, delete

from backend.src.api.dto import (
    ReportTemplateRequest,
    ReportTemplateRequestDTO,
    ReportTemplateResponse,
    ReportTemplateResponseDTO,
)
from backend.src.services import ReportTemplateService


class ReportTemplateController(Controller):
    @post(dto=ReportTemplateRequestDTO, return_dto=ReportTemplateResponseDTO)
    @inject
    async def create_template(
        self, data: ReportTemplateRequest, template_service: FromDishka[ReportTemplateService]
    ) -> ReportTemplateResponse:
        return await template_service.create_template(data)

    @get("/{template_id:int}", return_dto=ReportTemplateResponseDTO)
    @inject
    async def get_template(
        self, template_service: FromDishka[ReportTemplateService], template_id: int
    ) -> ReportTemplateResponse:
        return await template_service.get_template(template_id)

    @patch("/{template_id:int}", dto=ReportTemplateRequestDTO, return_dto=ReportTemplateResponseDTO)
    @inject
    async def update_template(
        self,
        template_service: FromDishka[ReportTemplateService],
        template_id: int,
        data: ReportTemplateRequest,
    ) -> ReportTemplateResponse:
        return await template_service.update_template(template_id, data)

    @delete("/{template_id:int}")
    @inject
    async def delete_template(
        self, template_service: FromDishka[ReportTemplateService], template_id: int
    ) -> None:
        await template_service.delete_template(template_id)
