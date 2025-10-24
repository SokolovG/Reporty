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
    AIModelRepository,
    AIProviderKeyRepository,
)
from backend.src.services import (
    ReportService,
    EncryptionService,
    AuthService,
    TaskService,
    SettingsService,
    RecordService,
    JWTService,
    NotificationService,
)


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
        user_repo: UserRepository,
    ) -> RecordService:
        return RecordService(record_repo=record_repo, user_repository=user_repo)

    @provide(scope=Scope.REQUEST)
    def ai_provider_repo(self, db_session: AsyncSession) -> AIProviderRepository:
        return AIProviderRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def ai_model_repo(self, db_session: AsyncSession) -> AIModelRepository:
        return AIModelRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def ai_key_repo(self, db_session: AsyncSession) -> AIProviderKeyRepository:
        return AIProviderKeyRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def external_system_repo(self, db_session: AsyncSession) -> ExternalSystemRepository:
        return ExternalSystemRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def report_service(
        self,
        report_repo: ReportRepository,
        record_repo: DailyRecordRepository,
        user_repo: UserRepository,
    ) -> ReportService:
        return ReportService(report_repo, record_repo, user_repository=user_repo)

    @provide(scope=Scope.REQUEST)
    def external_task_repo(self, db_session: AsyncSession) -> ExternalTaskRepository:
        return ExternalTaskRepository(session=db_session)

    @provide(scope=Scope.APP)
    def encryption_service(self) -> EncryptionService:
        return EncryptionService()

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
        external_system_repo: ExternalSystemRepository,
        ai_model_repo: AIModelRepository,
        user_repo: UserRepository,
        encryption_service: EncryptionService,
        api_key_repo: AIProviderKeyRepository,
    ) -> SettingsService:
        return SettingsService(
            ai_provider_repository=ai_provider_repo,
            ai_models_repository=ai_model_repo,
            external_system_repository=external_system_repo,
            user_repository=user_repo,
            encryption_service=encryption_service,
            api_key_repo=api_key_repo,
        )

    @provide(scope=Scope.REQUEST)
    def user_repository(self, db_session: AsyncSession) -> UserRepository:
        return UserRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def jwt_service(self) -> JWTService:
        return JWTService()

    @provide(scope=Scope.REQUEST)
    def notification_service(self) -> NotificationService:
        return NotificationService()

    @provide(scope=Scope.REQUEST)
    def auth_service(
        self,
        user_repo: UserRepository,
        jwt_service: JWTService,
        notification_service: NotificationService,
    ) -> AuthService:
        return AuthService(user_repo, jwt_service, notification_service)
