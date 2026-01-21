from datetime import datetime
import msgspec


class DailyReportRequest(msgspec.Struct):
    date: datetime = datetime.today()


class DailyReportRequestUpdate(msgspec.Struct):
    report_id: int
    # TODO: report update
