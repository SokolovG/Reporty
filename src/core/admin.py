from sqladmin import ModelView

from src.database.models import DailyRecord, Report


class ReportAdmin(ModelView, model=Report):
    column_list = [Report.report_date, Report.content, Report.generated_at]


class DailyRecordAdmin(ModelView, model=DailyRecord):
    column_list = [
        DailyRecord.raw_input,
        DailyRecord.ai_processed,
        DailyRecord.final_description,
        DailyRecord.created_at,
        DailyRecord.processed_at,
        DailyRecord.is_processed,
        DailyRecord.is_approved,
        DailyRecord.bitrix_task_id,
    ]
