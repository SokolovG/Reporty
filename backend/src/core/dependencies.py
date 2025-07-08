from typing import AsyncGenerator

from dishka import Scope, provide
from dishka.provider import Provider
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.config import get_sqlalchemy_config
from backend.src.database.repositories import (
    DailyRecordRepository,
    ReportRepository,
    ExternalSystemRepository,
    ExternalTaskRepository,
    ProfileRepository,
    UserSettingsRepository,
)
from backend.src.database.repositories.report_repository import ReportTemplateRepository
from backend.src.services import ReportService, CryptoService, ReportTemplateService
from backend.src.services.record_service import RecordService
from backend.src.services.task_service import TaskService
from backend.src.services.user_service import UserService
from backend.src.services.report_data_provider import ReportDataProvider


class MyProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        sqlalchemy_config = get_sqlalchemy_config()
        session_maker = sqlalchemy_config.create_session_maker()
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def record_repo(self, db_session: AsyncSession) -> DailyRecordRepository:
        return DailyRecordRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def report_repo(self, db_session: AsyncSession) -> ReportRepository:
        return ReportRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def record_service(
        self,
        record_repo: DailyRecordRepository,
        settings_repo: UserSettingsRepository,
        crypto_service: CryptoService,
    ) -> RecordService:
        return RecordService(record_repo, settings_repo, crypto_service)

    @provide(scope=Scope.REQUEST)
    def report_service(
        self,
        report_repo: ReportRepository,
        record_repo: DailyRecordRepository,
        report_template_service: ReportTemplateService,
        report_data_provider: ReportDataProvider,
        user_service: UserService,
        user_settings_repo: UserSettingsRepository,
    ) -> ReportService:
        return ReportService(
            report_repo,
            record_repo,
            report_template_service,
            report_data_provider,
            user_service,
            user_settings_repo,
        )

    @provide(scope=Scope.REQUEST)
    def external_task_repo(self, db_session: AsyncSession) -> ExternalTaskRepository:
        return ExternalTaskRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def external_system_repo(self, db_session: AsyncSession) -> ExternalSystemRepository:
        return ExternalSystemRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def profile_repo(self, db_session: AsyncSession) -> ProfileRepository:
        return ProfileRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def settings_repo(self, db_session: AsyncSession) -> UserSettingsRepository:
        return UserSettingsRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def crypto_service(self, db_session: AsyncSession) -> CryptoService:
        return CryptoService()

    @provide(scope=Scope.REQUEST)
    def task_service(
        self,
        external_task_repo: ExternalTaskRepository,
        external_system_repo: ExternalSystemRepository,
    ) -> TaskService:
        return TaskService(external_task_repo, external_system_repo)

    @provide(scope=Scope.REQUEST)
    def report_template_repo(self, db_session: AsyncSession) -> ReportTemplateRepository:
        return ReportTemplateRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def report_template_service(
        self, report_template_repo: ReportTemplateRepository
    ) -> ReportTemplateService:
        return ReportTemplateService(report_template_repo)

    @provide(scope=Scope.REQUEST)
    def report_data_provider(
        self, user_service: UserService, profile_repo: ProfileRepository
    ) -> ReportDataProvider:
        return ReportDataProvider(profile_repo)
