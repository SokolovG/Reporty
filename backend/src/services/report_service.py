from logging import getLogger

from backend.src.api.dto import (
    DailyReportRequest,
    DailyReportRequestUpdate,
    DailyReportResponse,
)
from backend.src.database.base import RecordStatus
from backend.src.database.repositories import (
    ReportRepository,
    DailyRecordRepository,
    UserSettingsRepository,
)
from backend.src.database.models import Report
from backend.src.services.report_template_service import ReportTemplateService
from backend.src.services.report_data_provider import ReportDataProvider
from jinja2 import Environment, TemplateSyntaxError, UndefinedError, select_autoescape, Template
from functools import lru_cache

logger = getLogger(__name__)


class ReportService:
    def __init__(
        self,
        report_repo: ReportRepository,
        record_repo: DailyRecordRepository,
        report_template_service: ReportTemplateService,
        report_data_provider: ReportDataProvider,
        user_settings_repo: UserSettingsRepository,
    ) -> None:
        self.repo = report_repo
        self.record_repo = record_repo
        self.report_template_service = report_template_service
        self.report_data_provider = report_data_provider
        self.user_settings_repo = user_settings_repo
        self.jinja_env = Environment(
            autoescape=select_autoescape(["html", "xml"]),
            enable_async=True,
        )

    @lru_cache(maxsize=32)
    def _get_template(self, template_content: str) -> Template:
        try:
            return self.jinja_env.from_string(template_content)
        except TemplateSyntaxError as e:
            logger.error(f"Jinja2 syntax error: {e}")
            raise

    async def _render_report(self, template_content: str, context: dict) -> str:
        try:
            template = self._get_template(template_content)
            return await template.render_async(**context)
        except (TemplateSyntaxError, UndefinedError) as e:
            logger.error(f"Jinja2 render error: {e}")
            raise

    async def create_report(self, data: DailyReportRequest) -> DailyReportResponse:
        today_records = await self.record_repo.get_records_by_date(
            target_date=data.date, user_id=data.user_id
        )
        open_records = await self.record_repo.get_records_by_status(
            status=RecordStatus.OPEN, user_id=data.user_id
        )
        set_ids = set()
        unique_records = []
        for record in list(open_records) + list(today_records):
            if record.id not in set_ids:
                set_ids.add(record.id)
                unique_records.append(record)
        logger.info(f"today record - {today_records}")
        logger.info(f"open records record - {open_records}")
        logger.info(f"tasks - {unique_records}")

        template_id = data.template_id
        if not template_id:
            user_settings = await self.user_settings_repo.get_by_user_id(data.user_id)
            template_id = getattr(user_settings, "default_report_template_id", None)
        if not template_id:
            logger.error("Report template not specified and not found in user settings.")
            raise ValueError("Report template not specified.")
        template_obj = await self.report_template_service.get_template(template_id)
        template_content = template_obj.template_content

        context = await self.report_data_provider.build_context(
            user_id=data.user_id,
            date=data.date,
            records=unique_records,
            custom_fields=data.custom_fields,
        )
        try:
            rendered = await self._render_report(template_content, context)
        except Exception as e:
            logger.error(f"Failed to render report: {e}")
            raise
        report = await self.repo.add(
            Report(
                report_date=data.date,
                content=rendered,
                entries_count=len(unique_records),
            )
        )
        await self.repo.session.commit()
        return DailyReportResponse(
            id=report.id,
            report_date=report.report_date,
            content=report.content,
            entries_count=report.entries_count,
            generated_at=report.generated_at,
        )

    async def get_report(self, report_id: int) -> DailyReportResponse:
        report = await self.repo.get(report_id)
        return DailyReportResponse(
            id=report.id,
            report_date=report.report_date,
            content=report.content,
            entries_count=report.entries_count,
            generated_at=report.generated_at,
        )

    async def delete_report(self, report_id: int) -> None:
        record = await self.repo.delete(report_id)  # noqa

    async def update_report(self, update_data: DailyReportRequestUpdate) -> None:
        pass
