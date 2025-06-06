import msgspec
from litestar.dto import DTOConfig, MsgspecDTO


class DailyReportRequest(msgspec.Struct):
    pass


class DailyReportRequestUpdate(msgspec.Struct):
    pass


class DailyReportResponse(msgspec.Struct):
    pass


class DailyReportRequestDTO(MsgspecDTO[DailyReportRequest]):
    config = DTOConfig()


class DailyReportResponseDTO(MsgspecDTO[DailyReportResponse]):
    config = DTOConfig()


class DailyReportRequestUpdateDTO(MsgspecDTO[DailyReportRequestUpdate]):
    config = DTOConfig(partial=True, exclude={"id"})
