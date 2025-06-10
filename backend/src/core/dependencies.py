from dishka import Scope, provide
from dishka.provider import Provider
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.repositories import (
    DailyRecordRepository,
    DailyReportRepository,
    ExternalSystemRepository,
    ExternalTaskRepository,
    ProfileRepository,
    UserSettingsRepository,
)
from backend.src.services import ReportService
from backend.src.services.record_service import RecordService


class MyProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def record_repo(self, db_session: AsyncSession) -> DailyRecordRepository:
        return DailyRecordRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def report_repo(self, db_session: AsyncSession) -> DailyReportRepository:
        return DailyReportRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def record_service(
        self, record_repo: DailyRecordRepository, settings_repo: UserSettingsRepository
    ) -> RecordService:
        return RecordService(record_repo, settings_repo)

    @provide(scope=Scope.REQUEST)
    def report_service(self, report_repo: DailyReportRepository) -> ReportService:
        return ReportService(report_repo)

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
