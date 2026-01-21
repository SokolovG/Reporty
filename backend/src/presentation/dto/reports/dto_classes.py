from litestar.dto import DTOConfig
from backend.src.api.dto.base import BaseMsgspecDTO
from backend.src.api.dto.reports.requests import (
    DailyReportRequest,
    DailyReportRequestUpdate,
)


class DailyReportRequestDTO(BaseMsgspecDTO[DailyReportRequest]):
    config = DTOConfig()


class DailyReportRequestUpdateDTO(BaseMsgspecDTO[DailyReportRequestUpdate]):
    config = DTOConfig(partial=True, exclude={"id"})
