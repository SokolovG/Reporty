from typing import AsyncGenerator, Type, TypeVar

from dishka import Scope, provide
from dishka.provider import Provider
from litestar import Litestar, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.requests import Request as StarletteRequest

from backend.src.application.ports.notification import (
    DefaultNotificationService,
    NotificationService,
)
from backend.src.application.ports.repositories import (
    IAIModelRepository,
    IAIProviderKeyRepository,
    IAIProviderRepository,
    IDailyRecordRepository,
    IExternalTaskRepository,
    IExternalSystemRepository,
    IReportRepository,
    ITaskTypeRepository,
    IUserRepository,
)
from backend.src.application.use_cases.ai.ai_preferences_use_cases import AIPreferencesUseCases
from backend.src.application.use_cases.ai.ai_use_cases import AIUseCases
from backend.src.application.use_cases.auth.auth_use_cases import AuthUseCase
from backend.src.application.use_cases.auth.user_use_cases import UserUseCases
from backend.src.application.use_cases.records.record_use_cases import RecordUseCases
from backend.src.application.use_cases.reports.report_use_cases import ReportUseCases
from backend.src.application.use_cases.settings.settings_use_cases import SettingsUseCases
from backend.src.application.use_cases.tasks.task_type_use_cases import TaskTypeUseCases
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
    @provide(scope=Scope.APP)
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        config = get_sqlalchemy_config()
        return config.create_session_maker()  # type: ignore

    @provide(scope=Scope.REQUEST)
    async def get_db_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    @provide(scope=Scope.REQUEST)
    def record_repo(self, db_session: AsyncSession, converter: Converter) -> IDailyRecordRepository:
        return DailyRecordRepository(session=db_session, converter=converter)

    @provide(scope=Scope.REQUEST)
    def report_repo(self, db_session: AsyncSession, converter: Converter) -> IReportRepository:
        return ReportRepository(session=db_session, converter=converter)

    @provide(scope=Scope.REQUEST)
    def record_use_cases(
        self,
        record_repo: IDailyRecordRepository,
        user_repo: IUserRepository,
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
    def task_type_repo(self, db_session: AsyncSession, converter: Converter) -> ITaskTypeRepository:
        return TaskTypeRepository(session=db_session, converter=converter)

    @provide(scope=Scope.REQUEST)
    def ai_provider_repo(
        self, db_session: AsyncSession, converter: Converter
    ) -> IAIProviderRepository:
        return AIProviderRepository(session=db_session, converter=converter)

    @provide(scope=Scope.REQUEST)
    def ai_model_repo(self, db_session: AsyncSession) -> IAIModelRepository:
        return AIModelRepository(session=db_session)

    @provide(scope=Scope.REQUEST)
    def ai_key_repo(
        self, db_session: AsyncSession, converter: Converter
    ) -> IAIProviderKeyRepository:
        return AIProviderKeyRepository(session=db_session, converter=converter)

    @provide(scope=Scope.REQUEST)
    def external_system_repo(
        self, db_session: AsyncSession, converter: Converter
    ) -> IExternalSystemRepository:
        return ExternalSystemRepository(session=db_session, converter=converter)

    @provide(scope=Scope.REQUEST)
    def report_use_cases(
        self,
        report_repo: IReportRepository,
        record_repo: IDailyRecordRepository,
        user_repo: IUserRepository,
        converter: Converter,
    ) -> ReportUseCases:
        return ReportUseCases(
            report_repo,
            record_repo,
            user_repository=user_repo,
            converter=converter,
        )

    @provide(scope=Scope.REQUEST)
    def external_task_repo(
        self, db_session: AsyncSession, converter: Converter
    ) -> IExternalTaskRepository:
        return ExternalTaskRepository(session=db_session, converter=converter)

    @provide(scope=Scope.APP)
    def encryption_service(self) -> EncryptionService:
        return EncryptionService()

    @provide(scope=Scope.REQUEST)
    def task_use_cases(
        self,
        external_task_repo: IExternalTaskRepository,
        external_system_repo: IExternalSystemRepository,
        user_repo: IUserRepository,
        converter: Converter,
    ) -> TasksUseCase:
        return TasksUseCase(
            external_task_repo, external_system_repo, user_repo, converter=converter
        )

    @provide(scope=Scope.REQUEST)
    def settings_use_cases(
        self,
        ai_provider_repo: IAIProviderRepository,
        external_system_repo: IExternalSystemRepository,
        ai_model_repo: IAIModelRepository,
        user_repo: IUserRepository,
        api_key_repo: IAIProviderKeyRepository,
        converter: Converter,
    ) -> SettingsUseCases:
        return SettingsUseCases(
            ai_provider_repository=ai_provider_repo,
            ai_models_repository=ai_model_repo,
            external_system_repository=external_system_repo,
            user_repository=user_repo,
            api_key_repo=api_key_repo,
            converter=converter,
        )

    @provide(scope=Scope.REQUEST)
    def user_repo(self, db_session: AsyncSession, converter: Converter) -> IUserRepository:
        return UserRepository(session=db_session, converter=converter)

    @provide(scope=Scope.APP)
    def jwt_service(self) -> JWTService:
        return JWTService()

    @provide(scope=Scope.REQUEST)
    def notification_service(self) -> NotificationService:
        return DefaultNotificationService()

    @provide(scope=Scope.REQUEST)
    def auth_use_case(
        self,
        user_repo: IUserRepository,
        jwt_service: JWTService,
        notification_service: NotificationService,
        converter: Converter,
    ) -> AuthUseCase:
        return AuthUseCase(user_repo, jwt_service, notification_service, converter)

    @provide(scope=Scope.REQUEST)
    def user_use_cases(
        self,
        user_repo: IUserRepository,
        converter: Converter,
    ) -> UserUseCases:
        return UserUseCases(
            user_repository=user_repo,
            converter=converter,
        )

    @provide(scope=Scope.APP)
    def converter(self) -> Converter:
        return Converter()

    @provide(scope=Scope.REQUEST)
    def ai_use_cases(
        self,
        encryption_service: EncryptionService,
        user_repo: IUserRepository,
        api_key_repo: IAIProviderKeyRepository,
    ) -> AIUseCases:
        return AIUseCases(encryption_service, user_repo, api_key_repo)

    @provide(scope=Scope.REQUEST)
    def task_type_use_cases(
        self,
        task_type_repo: ITaskTypeRepository,
        user_repo: IUserRepository,
        converter: Converter,
    ) -> TaskTypeUseCases:
        return TaskTypeUseCases(
            task_type_repository=task_type_repo,
            user_repository=user_repo,
            converter=converter,
        )

    @provide(scope=Scope.REQUEST)
    def ai_preferences_use_cases(
        self,
        user_repo: IUserRepository,
        encryption_service: EncryptionService,
        ai_provider_repo: IAIProviderRepository,
        ai_key_repo: IAIProviderKeyRepository,
    ) -> AIPreferencesUseCases:
        return AIPreferencesUseCases(
            user_repository=user_repo,
            encryption_service=encryption_service,
            ai_provider_repository=ai_provider_repo,
            ai_key_repo=ai_key_repo,
        )
