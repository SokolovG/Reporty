import msgspec
from litestar.dto import MsgspecDTO, DTOConfig


class ReportTemplateRequest(msgspec.Struct):
    name: str
    user_id: int
    template_content: str


class ReportTemplateResponse(msgspec.Struct):
    name: str
    user_id: int
    template_content: str


class ReportTemplateRequestDTO(MsgspecDTO[ReportTemplateRequest]):
    config = DTOConfig()


class ReportTemplateResponseDTO(MsgspecDTO[ReportTemplateResponse]):
    config = DTOConfig()
