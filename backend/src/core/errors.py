from enum import Enum


class ErrorCode(str, Enum):
    INVALID_CREDENTIALS = "AUTH_001"
    USER_ALREADY_EXISTS = "AUTH_002"
    INVALID_TOKEN = "AUTH_003"
    USER_NOT_EXIST = "AUTH_004"
