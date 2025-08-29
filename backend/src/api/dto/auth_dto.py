import msgspec

from backend.src.api.dto.base import BaseMsgspecDTO
from backend.src.api.responses.base_responses import SuccessResponse


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


class TokenInfo(msgspec.Struct):
    """Token information for authentication."""

    access: str
    refresh: str
    token_type: str


class SuccessResponseDTO(BaseMsgspecDTO[SuccessResponse]):
    pass
