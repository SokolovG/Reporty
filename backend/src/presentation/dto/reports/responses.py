from datetime import datetime

import msgspec


class ReportResponse(msgspec.Struct):
    id: int
    report_date: datetime
    content: str
    entries_count: int
    generated_at: datetime
