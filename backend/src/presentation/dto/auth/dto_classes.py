from litestar.dto import DTOConfig
from backend.src.api.dto.base import BaseMsgspecDTO
from backend.src.api.dto.auth.requests import (
    LoginRequest,
    RegisterRequest,
    UserUpdateRequest,
)


class LoginRequestDTO(BaseMsgspecDTO[LoginRequest]):
    pass


class RegisterRequestDTO(BaseMsgspecDTO[RegisterRequest]):
    pass


class UserUpdateRequestDTO(BaseMsgspecDTO[UserUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")
