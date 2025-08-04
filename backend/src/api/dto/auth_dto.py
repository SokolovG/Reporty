import msgspec

from backend.src.api.dto.base import BaseMsgspecDTO


class ChangePasswordRequest(msgspec.Struct):
    old_password: str
    new_password: str


class RefreshTokenRequest(msgspec.Struct):
    username: str


class LogoutRequest(msgspec.Struct):
    username: str


class LoginRequest(msgspec.Struct):
    username: str
    password: str


class RegisterRequest(msgspec.Struct):
    username: str
    password: str
    email: str | None = None


class LoginRequestDTO(BaseMsgspecDTO[LoginRequest]):
    pass


class RegisterRequestDTO(BaseMsgspecDTO[RegisterRequest]):
    pass


class LogoutRequestDTO(BaseMsgspecDTO[LogoutRequest]):
    pass


class RefreshTokenRequestSchemaDTO(BaseMsgspecDTO[RefreshTokenRequest]):
    pass


class ChangePasswordRequestSchemaDTO(BaseMsgspecDTO[ChangePasswordRequest]):
    pass
