from datetime import datetime

import msgspec


class ReportData(msgspec.Struct):
    date: datetime = datetime.today()


class ReportUpdateData(msgspec.Struct):
    report_id: int
    # TODO: report update
