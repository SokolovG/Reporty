from cryptography.utils import Enum


class RecordStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
