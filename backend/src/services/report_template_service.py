from backend.src.database.repositories.report_repository import ReportTemplateRepository
from backend.src.api.dto.profile_dto import ReportTemplateRequest, ReportTemplateResponse
from backend.src.database.models import ReportTemplate


class ReportTemplateService:
    def __init__(self, template_repo: ReportTemplateRepository):
        self.template_repo = template_repo

    async def create_template(self, data: ReportTemplateRequest) -> ReportTemplateResponse:
        template = ReportTemplate(
            name=data.name,
            user_id=data.user_id,
            template_content=data.template_content,
            is_active=True,
        )
        await self.template_repo.add(template)
        await self.template_repo.session.commit()
        return ReportTemplateResponse(
            name=template.name, user_id=template.user_id, template_content=template.template_content
        )

    async def get_template(self, template_id: int) -> ReportTemplateResponse:
        template = await self.template_repo.get(template_id)
        return ReportTemplateResponse(
            name=template.name, user_id=template.user_id, template_content=template.template_content
        )

    async def update_template(
        self, template_id: int, data: ReportTemplateRequest
    ) -> ReportTemplateResponse:
        template = await self.template_repo.get(template_id)
        template.name = data.name
        template.template_content = data.template_content
        template.is_active = True
        await self.template_repo.update(template)
        return ReportTemplateResponse(
            name=template.name, user_id=template.user_id, template_content=template.template_content
        )

    async def delete_template(self, template_id: int) -> None:
        await self.template_repo.delete(template_id)
