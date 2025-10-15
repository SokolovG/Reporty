import msgspec
from litestar.dto import DTOConfig

from backend.src.api.dto.base import BaseMsgspecDTO


class ChangePasswordRequest(msgspec.Struct):
    old_password: str
    new_password: str


class LogoutRequest(msgspec.Struct):
    email: str


class LoginRequest(msgspec.Struct):
    email: str
    password: str


class RegisterRequest(msgspec.Struct):
    name: str
    password: str
    email: str


class LoginRequestDTO(BaseMsgspecDTO[LoginRequest]):
    pass


class RegisterRequestDTO(BaseMsgspecDTO[RegisterRequest]):
    pass


class UserResponse(msgspec.Struct):
    """User data for API responses."""

    name: str
    email: str
    id: int
    is_active: bool
    is_verify: bool

    display_name: str | None = None
    department: str | None = None
    position: str | None = None
    ai_auto_process: bool = False
    ai_provider_id: int | None = None
    ai_model_id: int | None = None


class TokenInfo(msgspec.Struct):
    """Token information for authentication."""

    access: str
    refresh: str
    token_type: str


class UserUpdateRequest(msgspec.Struct):
    """Request to update user information."""

    display_name: str | None = None
    department: str | None = None
    position: str | None = None
    email: str | None = None


class AccessTokenResponse(msgspec.Struct):
    access_token: str


class UserUpdateRequestDTO(BaseMsgspecDTO[UserUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")
