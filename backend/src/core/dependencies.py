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
    UserRepository,
    AIProviderRepository,
    UserProfileRepository,
)
from backend.src.services import ReportService, CryptoService
from backend.src.services.record_service import RecordService
from backend.src.services.task_service import TaskService
from backend.src.services.settings_service import SettingsService


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
        user_profile_repo: UserProfileRepository,
        crypto_service: CryptoService,
    ) -> RecordService:
        return RecordService(record_repo, user_profile_repo, crypto_service)

    @provide(scope=Scope.REQUEST)
    def user_profile_repo(self, db_session: AsyncSession) -> UserProfileRepository:
        return UserProfileRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def ai_provider_repo(self, db_session: AsyncSession) -> AIProviderRepository:
        return AIProviderRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def external_system_repo(self, db_session: AsyncSession) -> ExternalSystemRepository:
        return ExternalSystemRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def report_service(
        self,
        report_repo: ReportRepository,
        record_repo: DailyRecordRepository,
        user_profile_repo: UserProfileRepository,
    ) -> ReportService:
        return ReportService(
            report_repo,
            record_repo,
            user_profile_repo,
        )

    @provide(scope=Scope.REQUEST)
    def external_task_repo(self, db_session: AsyncSession) -> ExternalTaskRepository:
        return ExternalTaskRepository(session=db_session)

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
    def settings_service(
        self,
        ai_provider_repo: AIProviderRepository,
        user_profile_repo: UserProfileRepository,
        external_system_repo: ExternalSystemRepository,
    ) -> SettingsService:
        return SettingsService(
            ai_provider_repo,
            user_profile_repo,
            external_system_repo,
        )

    @provide(scope=Scope.REQUEST)
    def user_repository(self, db_session: AsyncSession) -> UserRepository:
        return UserRepository(session=db_session)
