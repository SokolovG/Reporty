from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig
from msgspec import Struct

from backend.src.infrastructure.database.models import UserModel
from backend.src.presentation.dto.base import BaseMsgspecDTO


class UserRegistrationSchema(Struct):
    username: str
    password: str
    ai_provider_id: int
    display_name: str | None = None
    department: str | None = None
    position: str | None = None
    ai_auto_process: bool = False


class AuthenticationSchema(Struct):
    username: str
    password: str


class UserReadSchema(Struct):
    username: str
    user_id: int
    is_active: bool
    is_verified: bool
    ai_provider_id: int | None = None
    display_name: str | None = None
    department: str | None = None
    position: str | None = None
    ai_auto_process: bool = False


class UserRegistrationDTO(BaseMsgspecDTO[UserRegistrationSchema]):
    """User registration DTO with profile fields."""


class UserReadDTO(SQLAlchemyDTO[UserModel]):
    config = SQLAlchemyDTOConfig(exclude={"password_hash"}, rename_strategy="camel")


class UserUpdateDTO(SQLAlchemyDTO[UserModel]):
    config = SQLAlchemyDTOConfig(exclude={"password_hash"}, partial=True, rename_strategy="camel")
