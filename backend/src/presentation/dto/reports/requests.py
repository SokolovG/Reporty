from datetime import datetime

import msgspec


class ReportRequest(msgspec.Struct):
    date: datetime = datetime.today()


class ReportRequestUpdate(msgspec.Struct):
    report_id: int
    # TODO: report update
