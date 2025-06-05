from dishka import Scope, provide
from dishka.provider import Provider
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.repositories import (
    DailyRecordRepository,
    DailyReportRepository,
    ExternalSystemRepository,
    ExternalTaskRepository,
)
from src.services.record_service import RecordService


class MyProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def record_repo(self, db_session: AsyncSession) -> DailyRecordRepository:
        return DailyRecordRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def report_repo(self, db_session: AsyncSession) -> DailyReportRepository:
        return DailyReportRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def record_service(self, record_repo: DailyRecordRepository) -> RecordService:
        return RecordService(record_repo)

    @provide(scope=Scope.REQUEST)
    def external_task_repo(self, db_session: AsyncSession) -> ExternalTaskRepository:
        return ExternalTaskRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def external_system_repo(self, db_session: AsyncSession) -> ExternalSystemRepository:
        return ExternalSystemRepository(session=db_session)
