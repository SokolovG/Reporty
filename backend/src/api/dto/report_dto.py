from datetime import datetime

import msgspec
from litestar.dto import DTOConfig, MsgspecDTO


class DailyReportRequest(msgspec.Struct):
    date: datetime = datetime.today()
    user_id: int | None = None


class DailyReportRequestUpdate(msgspec.Struct):
    report_id: int


class DailyReportResponse(msgspec.Struct):
    pass


class DailyReportRequestDTO(MsgspecDTO[DailyReportRequest]):
    config = DTOConfig()


class DailyReportResponseDTO(MsgspecDTO[DailyReportResponse]):
    config = DTOConfig()


class DailyReportRequestUpdateDTO(MsgspecDTO[DailyReportRequestUpdate]):
    config = DTOConfig(partial=True, exclude={"id"})
