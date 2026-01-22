from litestar.dto import DTOConfig

from backend.src.application.dto.reports import ReportData
from backend.src.presentation.dto.base import BaseMsgspecDTO


class ReportRequestDTO(BaseMsgspecDTO[ReportData]):
    config = DTOConfig()


class ReportRequestUpdateDTO(BaseMsgspecDTO[ReportData]):
    config = DTOConfig(partial=True, exclude={"id"})
