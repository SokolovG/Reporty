from dishka import Scope, provide
from dishka.provider import Provider
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.repositories import DailyRecordRepository, DailyReportRepository


class MyProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def record_repo(self, db_session: AsyncSession) -> DailyRecordRepository:
        return DailyRecordRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def report_repo(self, db_session: AsyncSession) -> DailyReportRepository:
        return DailyReportRepository(session=db_session)
