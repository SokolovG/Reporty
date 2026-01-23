from typing import AsyncGenerator, Type, TypeVar

from dishka import Scope, provide
from dishka.provider import Provider
from litestar import Litestar, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request as StarletteRequest

from backend.src.application.ports.notification import (
    DefaultNotificationService,
    NotificationService,
)
from backend.src.application.use_cases.ai.ai_use_cases import AIUseCases
from backend.src.application.use_cases.auth.auth_use_cases import AuthUseCase
from backend.src.application.use_cases.auth.user_use_cases import UserUseCases
from backend.src.application.use_cases.records.record_use_cases import RecordUseCases
from backend.src.application.use_cases.reports.report_use_cases import ReportUseCases
from backend.src.application.use_cases.settings.settings_use_cases import SettingsUseCases
from backend.src.application.use_cases.tasks.tasks_use_cases import TasksUseCase
from backend.src.infrastructure.config.configs import get_sqlalchemy_config
from backend.src.infrastructure.database.mappers import Converter
from backend.src.infrastructure.database.repositories import (
    AIModelRepository,
    AIProviderKeyRepository,
    AIProviderRepository,
    DailyRecordRepository,
    ExternalSystemRepository,
    ExternalTaskRepository,
    ReportRepository,
    TaskTypeRepository,
    UserRepository,
)
from backend.src.infrastructure.encryption.encryption_service import EncryptionService
from backend.src.infrastructure.encryption.jwt_service import JWTService

T = TypeVar("T")


async def get_dependency(request: Request | StarletteRequest, dependency_type: Type[T]) -> T:
    """Helper to get dependencies from Dishka via Starlette request."""
    litestar_app = Litestar.from_scope(request.scope)  # type:ignore
    container = litestar_app.state.dishka_container

    async with container() as request_container:
        obj: T = await request_container.get(dependency_type)
        return obj


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
    def record_use_cases(
        self,
        record_repo: DailyRecordRepository,
        user_repo: UserRepository,
        ai_use_cases: AIUseCases,
        converter: Converter,
    ) -> RecordUseCases:
        return RecordUseCases(
            record_repo=record_repo,
            user_repository=user_repo,
            ai_use_cases=ai_use_cases,
            converter=converter,
        )

    @provide(scope=Scope.REQUEST)
    def task_type_repo(self, db_session: AsyncSession) -> TaskTypeRepository:
        return TaskTypeRepository(session=db_session)

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
    def report_use_cases(
        self,
        report_repo: ReportRepository,
        record_repo: DailyRecordRepository,
        user_repo: UserRepository,
        converter: Converter,
    ) -> ReportUseCases:
        return ReportUseCases(
            report_repo,
            record_repo,
            user_repository=user_repo,
            converter=converter,
        )

    @provide(scope=Scope.REQUEST)
    def external_task_repo(self, db_session: AsyncSession) -> ExternalTaskRepository:
        return ExternalTaskRepository(session=db_session)

    @provide(scope=Scope.APP)
    def encryption_service(self) -> EncryptionService:
        return EncryptionService()

    @provide(scope=Scope.REQUEST)
    def task_use_casess(
        self,
        external_task_repo: ExternalTaskRepository,
        external_system_repo: ExternalSystemRepository,
        user_repo: UserRepository,
        converter: Converter,
    ) -> TasksUseCase:
        return TasksUseCase(
            external_task_repo, external_system_repo, user_repo, converter=converter
        )

    @provide(scope=Scope.REQUEST)
    def settings_use_cases(
        self,
        ai_provider_repo: AIProviderRepository,
        external_system_repo: ExternalSystemRepository,
        ai_model_repo: AIModelRepository,
        user_repo: UserRepository,
        encryption_service: EncryptionService,
        api_key_repo: AIProviderKeyRepository,
        converter: Converter,
    ) -> SettingsUseCases:
        return SettingsUseCases(
            ai_provider_repository=ai_provider_repo,
            ai_models_repository=ai_model_repo,
            external_system_repository=external_system_repo,
            user_repository=user_repo,
            encryption_service=encryption_service,
            api_key_repo=api_key_repo,
            converter=converter,
        )

    @provide(scope=Scope.REQUEST)
    def user_repository(self, db_session: AsyncSession) -> UserRepository:
        return UserRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def jwt_service(self) -> JWTService:
        return JWTService()

    @provide(scope=Scope.REQUEST)
    def notification_service(self) -> NotificationService:
        return DefaultNotificationService()

    @provide(scope=Scope.REQUEST)
    def auth_use_case(
        self,
        user_repo: UserRepository,
        jwt_service: JWTService,
        notification_service: NotificationService,
        converter: Converter,
    ) -> AuthUseCase:
        return AuthUseCase(user_repo, jwt_service, notification_service, converter)

    @provide(scope=Scope.REQUEST)
    def user_use_cases(
        self,
        user_repo: UserRepository,
        ai_provider_repo: AIProviderRepository,
        ai_model_repo: AIModelRepository,
        external_system_repo: ExternalSystemRepository,
        encryption_service: EncryptionService,
        ai_key_repo: AIProviderKeyRepository,
        converter: Converter,
    ) -> UserUseCases:
        return UserUseCases(
            ai_provider_repository=ai_provider_repo,
            ai_models_repository=ai_model_repo,
            user_repository=user_repo,
            external_system_repository=external_system_repo,
            encryption_service=encryption_service,
            api_key_repo=ai_key_repo,
            converter=converter,
        )

    @provide(scope=Scope.APP)
    def converter() -> Converter:
        return Converter()

    @provide(scope=Scope.REQUEST)
    def ai_use_cases(
        self,
        encryption_service: EncryptionService,
        user_repo: UserRepository,
        api_key_repo: AIProviderKeyRepository,
    ) -> AIUseCases:
        return AIUseCases(encryption_service, user_repo, api_key_repo)
