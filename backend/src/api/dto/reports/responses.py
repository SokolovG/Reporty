from datetime import datetime
import msgspec


class DailyReportResponse(msgspec.Struct):
    id: int
    report_date: datetime
    content: str
    entries_count: int
    generated_at: datetime
