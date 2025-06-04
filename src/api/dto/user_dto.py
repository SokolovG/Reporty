from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig
from litestar.dto import MsgspecDTO
from msgspec import Struct

from src.database.models import User


class UserRegistrationSchema(Struct):
    email: str
    password: str


class UserRegistrationDTO(MsgspecDTO[UserRegistrationSchema]):
    """User registration DTO."""


class UserReadDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"password_hash"})


class UserUpdateDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"password_hash"}, partial=True)
