import msgspec
from litestar.dto import DTOConfig, MsgspecDTO


class DailyReportRequest(msgspec.Struct):
    pass


class DailyReportResponse(msgspec.Struct):
    pass


class DailyReportRequestDTO(MsgspecDTO[DailyReportRequest]):
    config = DTOConfig()


class DailyReportResponseDTO(MsgspecDTO[DailyReportResponse]):
    config = DTOConfig()
