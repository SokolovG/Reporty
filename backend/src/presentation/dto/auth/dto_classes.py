from litestar.dto import DTOConfig

from backend.src.presentation.dto.auth.requests import (
    LoginRequest,
    RegisterRequest,
    UserUpdateRequest,
)
from backend.src.presentation.dto.base import BaseMsgspecDTO


class LoginRequestDTO(BaseMsgspecDTO[LoginRequest]):
    pass


class RegisterRequestDTO(BaseMsgspecDTO[RegisterRequest]):
    pass


class UserUpdateRequestDTO(BaseMsgspecDTO[UserUpdateRequest]):
    config = DTOConfig(partial=True, rename_strategy="camel")
