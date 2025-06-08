from sqladmin import ModelView

from backend.src.database.models import (
    DailyRecord,
    ExternalSystem,
    ExternalTask,
    Report,
    User,
)


class ReportAdmin(ModelView, model=Report):
    column_list = [Report.report_date, Report.content, Report.generated_at]


class UserAdmin(ModelView, model=User):
    column_list = [
        User.email,
        User.is_active,
        User.created_at,
        User.id,
        User.is_verified,
    ]


class DailyRecordAdmin(ModelView, model=DailyRecord):
    column_list = [
        DailyRecord.raw_input,
        DailyRecord.ai_processed,
        DailyRecord.final_description,
        DailyRecord.created_at,
        DailyRecord.processed_at,
        DailyRecord.is_processed,
        DailyRecord.is_approved,
        DailyRecord.external_task_id,
    ]


class ExternalSystemAdmin(ModelView, model=ExternalSystem):
    column_list = [
        ExternalSystem.name,
        ExternalSystem.display_name,
        ExternalSystem.api_config,
        ExternalSystem.is_active,
    ]


class ExternalTaskAdmin(ModelView, model=ExternalTask):
    column_list = [
        ExternalTask.external_id,
        ExternalTask.external_system_id,
        ExternalTask.title,
        ExternalTask.description,
        ExternalTask.status,
        ExternalTask.external_created_at,
        ExternalTask.external_updated_at,
        ExternalTask.completed_at,
        ExternalTask.last_sync,
        ExternalTask.system,
    ]
