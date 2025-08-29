from markupsafe import Markup
from sqladmin import ModelView

from backend.src.database.models import (
    DailyRecord,
    ExternalSystem,
    ExternalTask,
    Report,
    User,
    UserProfile,
    TaskType,
    AIProvider,
)


class ReportAdmin(ModelView, model=Report):
    name = "Report"
    name_plural = "Reports"
    icon = "fa-solid fa-file-lines"
    column_list = [Report.id, Report.report_date, Report.content, Report.generated_at]
    column_formatters = {"content": lambda m, a: Markup(m.content.replace("\n", "<br>"))}  # type:ignore


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    column_exclude_list = [User.password_hash]


class DailyRecordAdmin(ModelView, model=DailyRecord):
    name = "Daily Record"
    name_plural = "Daily Records"
    icon = "fa-solid fa-book"
    column_list = [
        DailyRecord.id,
        DailyRecord.title,
        DailyRecord.status,
        DailyRecord.raw_input,
        DailyRecord.ai_processed,
        DailyRecord.final_description,
        DailyRecord.created_at,
        DailyRecord.processed_at,
        DailyRecord.is_processed,
        DailyRecord.is_approved,
        DailyRecord.external_url,
        "external_task.url",
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
        ExternalTask.id,
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
        ExternalTask.url,
    ]


class UserProfileAdmin(ModelView, model=UserProfile):
    name = "Profile"
    name_plural = "Profiles"
    icon = "fa-solid fa-id-card"
    column_list = [
        UserProfile.id,
        UserProfile.user_id,
        UserProfile.display_name,
        UserProfile.department,
        UserProfile.position,
        UserProfile.ai_auto_process,
    ]


class TaskTypeAdmin(ModelView, model=TaskType):
    name = "Task type"
    name_plural = "Task types"

    column_list = [
        TaskType.id,
        TaskType.user_id,
        TaskType.title,
        TaskType.color,
        TaskType.is_active,
        TaskType.user_profile_id,
    ]
    form_columns = [
        TaskType.id,
        TaskType.user_id,
        TaskType.title,
        TaskType.color,
        TaskType.is_active,
        TaskType.user_profile_id,
    ]


class AIProviderAdmin(ModelView, model=AIProvider):
    name = "AI provider"
    name_plural = "AI providers"

    column_list = [
        AIProvider.id,
        AIProvider.name,
        AIProvider.base_prompt,
        AIProvider.model_name,
        AIProvider.requires_api_key,
        AIProvider.encrypted_api_key,
        AIProvider.is_active,
    ]
