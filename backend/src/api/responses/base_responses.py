from typing import Any

import msgspec


class BaseErrorResponse(msgspec.Struct):
    error_code: str


class BaseErrorDetails(msgspec.Struct):
    reason: str
    context: dict[str, Any] = {}
