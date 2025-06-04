from datetime import datetime
from uuid import UUID

import msgspec


class DailyRecordRequest(msgspec.Struct):
    raw_input: str
    bitrix_task_id: str | None = None


class DailyRecordResponse(msgspec.Struct):
    id: UUID
    raw_input: str
    ai_processed: str | None
    final_description: str | None
    created_at: datetime
    processed_at: datetime | None
    is_processed: bool
    is_approved: bool
    bitrix_task_id: str | None
