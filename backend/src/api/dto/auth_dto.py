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
    email: str


class LoginRequestDTO(BaseMsgspecDTO[LoginRequest]):
    pass


class RegisterRequestDTO(BaseMsgspecDTO[RegisterRequest]):
    pass


class UserResponse(msgspec.Struct):
    username: str
    email: str
    user_id: int
    is_active: bool
    is_verified: bool


class FailedLoginResponse(msgspec.Struct):
    pass


class SuccessLogoutResponse(msgspec.Struct):
    pass


class SuccessLoginResponse(msgspec.Struct):
    pass


class SuccessRefreshResponse(msgspec.Struct):
    pass


class FailedRefreshResponse(msgspec.Struct):
    pass


class SuccessChangePasswordResponse(msgspec.Struct):
    pass


class FailedChangePasswordResponse(msgspec.Struct):
    pass


class LogoutRequestDTO(BaseMsgspecDTO[LogoutRequest]):
    pass


class RefreshTokenRequestSchemaDTO(BaseMsgspecDTO[RefreshTokenRequest]):
    pass


class ChangePasswordRequestSchemaDTO(BaseMsgspecDTO[ChangePasswordRequest]):
    pass
