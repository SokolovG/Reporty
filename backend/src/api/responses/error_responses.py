from backend.src.api.responses.base_responses import BaseErrorResponse, BaseErrorDetails


class ErrorResponse(BaseErrorResponse):
    msg: str
    details: BaseErrorDetails
