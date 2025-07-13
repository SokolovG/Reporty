from typing import TypeVar
from litestar.dto import MsgspecDTO, DTOConfig

T = TypeVar("T")


class BaseMsgspecDTO(MsgspecDTO[T]):  # type: ignore
    config = DTOConfig(rename_strategy="camel")
