from typing import TypeVar

from litestar.dto import MsgspecDTO, DTOConfig
from msgspec import Struct


T = TypeVar("T", bound=Struct)


class BaseMsgspecDTO(MsgspecDTO[T]):
    config = DTOConfig(rename_strategy="camel")
