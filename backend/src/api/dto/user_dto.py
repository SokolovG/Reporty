from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig
from msgspec import Struct

from backend.src.api.dto.base import BaseMsgspecDTO
from backend.src.database.models import User


class UserRegistrationSchema(Struct):
    username: str
    password: str


class AuthenticationSchema(Struct):
    username: str
    password: str


class UserReadSchema(Struct):
    username: str
    user_id: int
    is_active: bool
    is_verified: bool


class UserRegistrationDTO(BaseMsgspecDTO[UserRegistrationSchema]):
    """User registration DTO."""


class UserReadDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"password_hash"}, rename_strategy="camel")


class UserUpdateDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"password_hash"}, partial=True, rename_strategy="camel")
