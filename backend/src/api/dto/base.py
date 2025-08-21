from typing import TypeVar
from litestar.dto import MsgspecDTO, DTOConfig

T = TypeVar("T")


class BaseMsgspecDTO(MsgspecDTO[T]):
    config = DTOConfig(rename_strategy="camel")
