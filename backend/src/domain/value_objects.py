from dataclasses import dataclass
from enum import Enum


class RecordStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass
class TokenPair:
    """Domain value object representing authentication tokens."""

    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
