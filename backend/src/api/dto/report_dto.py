from datetime import datetime

import msgspec
from litestar.dto import DTOConfig, MsgspecDTO


class DailyReportRequest(msgspec.Struct):
    user_id: int
    date: datetime = datetime.today()
    custom_fields: dict[str, str] = {}
    template_id: int | None = None


class DailyReportRequestUpdate(msgspec.Struct):
    report_id: int


class DailyReportResponse(msgspec.Struct):
    id: int
    report_date: datetime
    content: str
    entries_count: int
    generated_at: datetime


class DailyReportRequestDTO(MsgspecDTO[DailyReportRequest]):
    config = DTOConfig()


class DailyReportResponseDTO(MsgspecDTO[DailyReportResponse]):
    config = DTOConfig()


class DailyReportRequestUpdateDTO(MsgspecDTO[DailyReportRequestUpdate]):
    config = DTOConfig(partial=True, exclude={"id"})
