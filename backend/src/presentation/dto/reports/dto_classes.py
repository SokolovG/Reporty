from litestar.dto import DTOConfig

from backend.src.presentation.dto.base import BaseMsgspecDTO
from backend.src.presentation.dto.reports.requests import ReportRequest, ReportRequestUpdate


class ReportRequestDTO(BaseMsgspecDTO[ReportRequest]):
    config = DTOConfig()


class ReportRequestUpdateDTO(BaseMsgspecDTO[ReportRequestUpdate]):
    config = DTOConfig(partial=True, exclude={"id"})
