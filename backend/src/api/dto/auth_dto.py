import msgspec

from backend.src.api.dto.base import BaseMsgspecDTO


class ChangePasswordRequest(msgspec.Struct):
    old_password: str
    new_password: str


class RefreshTokenRequest(msgspec.Struct):
    email: str


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
    name: str
    email: str
    user_id: int
    is_active: bool
    is_verified: bool


class FailedLoginResponse(msgspec.Struct):
    pass


class SuccessLogoutResponse(msgspec.Struct):
    pass


class SuccessLoginResponse(msgspec.Struct):
    access: str


class TokenInfo(msgspec.Struct):
    access: str
    token_type: str


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


class TokenInfoDTO(BaseMsgspecDTO[TokenInfo]):
    pass


class ChangePasswordRequestSchemaDTO(BaseMsgspecDTO[ChangePasswordRequest]):
    pass
