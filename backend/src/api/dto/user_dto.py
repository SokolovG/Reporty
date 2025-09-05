from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig
from msgspec import Struct

from backend.src.api.dto.base import BaseMsgspecDTO
from backend.src.database.models import User


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
    display_name: str | None = None
    department: str | None = None
    position: str | None = None
    ai_auto_process: bool = False
    ai_provider_id: int


class UserProfileUpdateSchema(Struct):
    display_name: str | None = None
    department: str | None = None
    position: str | None = None
    ai_auto_process: bool | None = None
    ai_provider_id: int | None = None


class UserRegistrationDTO(BaseMsgspecDTO[UserRegistrationSchema]):
    """User registration DTO with profile fields."""


class UserReadDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"password_hash"}, rename_strategy="camel")


class UserUpdateDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"password_hash"}, partial=True, rename_strategy="camel")


class UserProfileUpdateDTO(BaseMsgspecDTO[UserProfileUpdateSchema]):
    """User profile update DTO."""
