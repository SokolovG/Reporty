from datetime import datetime

import msgspec
from litestar.dto import DTOConfig

from backend.src.api.dto.base import BaseMsgspecDTO


class DailyReportRequest(msgspec.Struct):
    date: datetime = datetime.today()
    custom_fields: dict[str, str] = {}


class DailyReportRequestUpdate(msgspec.Struct):
    report_id: int


class DailyReportResponse(msgspec.Struct):
    id: int
    report_date: datetime
    content: str
    entries_count: int
    generated_at: datetime


class DailyReportRequestDTO(BaseMsgspecDTO[DailyReportRequest]):
    config = DTOConfig()


class DailyReportResponseDTO(BaseMsgspecDTO[DailyReportResponse]):
    config = DTOConfig()


class DailyReportRequestUpdateDTO(BaseMsgspecDTO[DailyReportRequestUpdate]):
    config = DTOConfig(partial=True, exclude={"id"})
