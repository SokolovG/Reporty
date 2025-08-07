from backend.src.api.responses.base_responses import BaseErrorResponse, BaseErrorDetails


class FailResponse(BaseErrorResponse):
    msg: str
    details: BaseErrorDetails
