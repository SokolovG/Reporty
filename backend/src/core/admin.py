from sqladmin import ModelView

from backend.src.database.models import (
    DailyRecord,
    ExternalSystem,
    ExternalTask,
    Report,
    User,
    Profile,
)


class ReportAdmin(ModelView, model=Report):
    name = "Report"
    name_plural = "Reports"
    icon = "fa-solid fa-file-lines"
    column_list = [Report.report_date, Report.content, Report.generated_at]


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    column_list = [
        User.email,
        User.is_active,
        User.created_at,
        User.id,
        User.is_verified,
    ]


class DailyRecordAdmin(ModelView, model=DailyRecord):
    name = "Daily Record"
    name_plural = "Daily Records"
    icon = "fa-solid fa-book"
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
    name = "External System"
    name_plural = "External Systems"
    icon = "fa-solid fa-plug"
    column_list = [
        ExternalSystem.name,
        ExternalSystem.display_name,
        ExternalSystem.api_config,
        ExternalSystem.is_active,
    ]


class ExternalTaskAdmin(ModelView, model=ExternalTask):
    name = "External Task"
    name_plural = "External Tasks"
    icon = "fa-solid fa-tasks"
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


class ProfileAdmin(ModelView, model=Profile):
    column_list = [
        Profile.id,
        Profile.name,
    ]
