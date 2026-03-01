from datetime import datetime

import msgspec


class ReportData(msgspec.Struct):
    date: datetime | None = None


class ReportUpdateData(msgspec.Struct):
    report_id: int
    content: str | None = None
