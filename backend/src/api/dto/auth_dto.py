import msgspec

from backend.src.api.dto.base import BaseMsgspecDTO


class ChangePasswordRequest(msgspec.Struct):
    pass


class RefreshTokenRequest(msgspec.Struct):
    pass


class LogoutRequest(msgspec.Struct):
    pass


class LoginRequest(msgspec.Struct):
    pass


class LoginRequestDTO(BaseMsgspecDTO[LoginRequest]):
    pass


class RegisterRequest(msgspec.Struct):
    pass


class RegisterRequestDTO(BaseMsgspecDTO[RegisterRequest]):
    pass


class LogoutRequestDTO(BaseMsgspecDTO[LogoutRequest]):
    pass


class RefreshTokenRequestSchemaDTO(BaseMsgspecDTO[RefreshTokenRequest]):
    pass


class ChangePasswordRequestSchemaDTO(BaseMsgspecDTO[ChangePasswordRequest]):
    pass
