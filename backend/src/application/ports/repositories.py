from datetime import date
from typing import Protocol

from backend.src.application.dto.auth import UserData
from backend.src.application.dto.records import DailyRecordData, ExternalTaskCreateData
from backend.src.application.dto.reports import ReportUpdateData
from backend.src.domain.entities.ai import AIProvider, AIProviderKey
from backend.src.domain.entities.external_system import ExternalSystem
from backend.src.domain.entities.external_task import ExternalTask
from backend.src.domain.entities.record import DailyRecord
from backend.src.domain.entities.report import Report
from backend.src.domain.entities.task_type import TaskType
from backend.src.domain.entities.user import User
from backend.src.infrastructure.database.base import RecordStatus


class IAIProviderRepository(Protocol):
    async def get_active_providers_with_models(self) -> list[AIProvider]: ...

    async def get_by_id_with_models(self, provider_id: int) -> AIProvider | None: ...


class IAIModelRepository(Protocol): ...


class IAIProviderKeyRepository(Protocol):
    async def get_user_provider_key(
        self, user_id: int, provider_id: int
    ) -> AIProviderKey | None: ...


class IUserRepository(Protocol):
    async def create_user(self, user_data: UserData) -> User: ...

    async def update_profile(
        self,
        user_id: int,
        display_name: str | None = None,
        department: str | None = None,
        position: str | None = None,
        email: str | None = None,
    ) -> User: ...


class IExternalSystemRepository(Protocol):
    async def get_external_systems(self) -> list[ExternalSystem]: ...
    async def create_external_system(
        self, data: ExternalTaskCreateData, user_id: int
    ) -> ExternalTask: ...

    async def get_active_external_systems(self) -> list[ExternalSystem]: ...


class IExternalTaskRepository(Protocol):
    """Repository for managing external tasks."""

    async def get_by_external_id(
        self, system_id: int, external_id: int, user_id: int
    ) -> ExternalTask | None: ...

    async def get_tasks_for_sync(self, system_id: int) -> list[ExternalTask]:
        """Get tasks that need synchronization."""
        ...

    async def get_task(self, system_id: int, user_id: int) -> ExternalTask: ...


class IDailyRecordRepository(Protocol):
    async def create_record(self, data: DailyRecordData, user_id: int) -> DailyRecord: ...

    async def get_record(self, record_id: int, user_id: int) -> DailyRecord: ...

    async def get_by_title_user_and_date(
        self, title: str, user_id: int, day: date
    ) -> DailyRecord | None: ...

    async def get_with_external_task(self, record_id: int, user_id: int) -> DailyRecord: ...

    async def get_records_by_date(
        self, target_date: date, user_id: int, include_external_tasks: bool = False
    ) -> list[DailyRecord]: ...

    async def get_unprocessed_records(self, user_id: int) -> list[DailyRecord]: ...

    async def get_records_for_external_task(
        self, external_task_id: int, user_id: int
    ) -> list[DailyRecord]: ...

    async def get_records_by_status(
        self, status: RecordStatus, user_id: int
    ) -> list[DailyRecord]: ...

    async def get_all_records(self, user_id: int) -> list[DailyRecord]: ...


class IReportRepository(Protocol):
    async def get_latest_report(self, user_id: int) -> Report | None: ...

    async def get_reports_by_date_range(
        self, start_date: date, end_date: date, user_id: int
    ) -> list[Report]: ...

    async def update_report(self, update_data: ReportUpdateData, user_id: int) -> Report: ...

    async def get_report(self, report_id: int, user_id: int) -> Report: ...


class ITaskTypeRepository(Protocol):
    """Repository for TaskType operations."""

    async def get_all_for_user(self, user_id: int) -> list[TaskType]: ...

    async def get_by_id_and_user(self, task_type_id: int, user_id: int) -> TaskType: ...
    async def create_for_user(
        self, user_id: int, title: str, color: str | None = None
    ) -> TaskType: ...
