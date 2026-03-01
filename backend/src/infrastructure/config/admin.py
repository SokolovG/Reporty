from markupsafe import Markup
from sqladmin import ModelView

from backend.src.infrastructure.database.models import (
    AIModel,
    AIProviderModel,
    DailyRecordModel,
    ExternalSystemModel,
    ExternalTaskModel,
    ReportModel,
    TaskTypeModel,
    UserModel,
)


class ReportAdmin(ModelView, model=ReportModel):
    name = "Report"
    name_plural = "Reports"
    icon = "fa-solid fa-file-lines"
    column_list = [
        ReportModel.id,
        ReportModel.report_date,
        ReportModel.content,
        ReportModel.generated_at,
    ]
    column_formatters = {"content": lambda m, a: Markup(m.content.replace("\n", "<br>"))}


class UserAdmin(ModelView, model=UserModel):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    form_include_pk = True
    column_list = [
        UserModel.id,
        UserModel.name,
        UserModel.email,
        UserModel.display_name,
        UserModel.department,
        UserModel.position,
        UserModel.ai_auto_process,
        UserModel.ai_provider_id,
        UserModel.task_types,
        UserModel.is_active,
        UserModel.ai_model_id,
        UserModel.custom_prompt,
        UserModel.is_verify,
        UserModel.is_admin,
    ]

    form_columns = [
        UserModel.name,
        UserModel.email,
        UserModel.display_name,
        UserModel.department,
        UserModel.position,
        UserModel.ai_auto_process,
        UserModel.ai_provider_id,
        UserModel.ai_model_id,
        UserModel.custom_prompt,
        UserModel.task_types,
        UserModel.is_active,
        UserModel.is_verify,
        UserModel.is_admin,
    ]


class DailyRecordAdmin(ModelView, model=DailyRecordModel):
    name = "Daily Record"
    name_plural = "Daily Records"
    icon = "fa-solid fa-book"
    form_include_pk = True
    column_list = [
        DailyRecordModel.id,
        DailyRecordModel.user_id,
        DailyRecordModel.title,
        DailyRecordModel.status,
        DailyRecordModel.raw_input,
        DailyRecordModel.ai_processed,
        DailyRecordModel.final_description,
        DailyRecordModel.is_processed,
        DailyRecordModel.is_approved,
        DailyRecordModel.external_url,
        "external_task.url",
    ]

    form_columns = [
        DailyRecordModel.user_id,
        DailyRecordModel.title,
        DailyRecordModel.status,
        DailyRecordModel.raw_input,
        DailyRecordModel.ai_processed,
        DailyRecordModel.final_description,
        DailyRecordModel.is_processed,
        DailyRecordModel.is_approved,
    ]


class ExternalSystemAdmin(ModelView, model=ExternalSystemModel):
    name = "External System"
    name_plural = "External Systems"
    icon = "fa-solid fa-plug"
    column_list = [
        ExternalSystemModel.name,
        ExternalSystemModel.display_name,
        ExternalSystemModel.api_config,
        ExternalSystemModel.is_active,
    ]


class ExternalTaskAdmin(ModelView, model=ExternalTaskModel):
    name = "External Task"
    name_plural = "External Tasks"
    icon = "fa-solid fa-tasks"
    column_list = [
        ExternalTaskModel.id,
        ExternalTaskModel.external_id,
        ExternalTaskModel.external_system_id,
        ExternalTaskModel.title,
        ExternalTaskModel.description,
        ExternalTaskModel.status,
        ExternalTaskModel.external_created_at,
        ExternalTaskModel.external_updated_at,
        ExternalTaskModel.completed_at,
        ExternalTaskModel.last_sync,
        ExternalTaskModel.system,
        ExternalTaskModel.url,
    ]


class TaskTypeAdmin(ModelView, model=TaskTypeModel):
    name = "Task type"
    name_plural = "Task types"
    form_include_pk = True
    column_list = [
        TaskTypeModel.id,
        TaskTypeModel.user_id,
        TaskTypeModel.title,
        TaskTypeModel.color,
        TaskTypeModel.is_active,
    ]
    form_columns = [
        TaskTypeModel.user_id,
        TaskTypeModel.title,
        TaskTypeModel.color,
        TaskTypeModel.is_active,
    ]


class AIProviderAdmin(ModelView, model=AIProviderModel):
    name = "AI provider"
    name_plural = "AI providers"

    column_list = [
        AIProviderModel.id,
        AIProviderModel.name,
        AIProviderModel.base_prompt,
        AIProviderModel.requires_api_key,
        AIProviderModel.is_active,
        AIProviderModel.models,
    ]


class AIModelAdmin(ModelView, model=AIModel):
    name = "AI model"
    name_plural = "AI models"

    column_list = [AIModel.id, AIModel.name, AIModel.ai_provider_id, AIModel.created_at]
