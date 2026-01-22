from litestar.dto import DTOConfig

from backend.src.application.dto.auth import LoginData, RegisterData, UpdateUserData
from backend.src.presentation.dto.base import BaseMsgspecDTO


class LoginRequestDTO(BaseMsgspecDTO[LoginData]):
    pass


class RegisterRequestDTO(BaseMsgspecDTO[RegisterData]):
    pass


class UserUpdateRequestDTO(BaseMsgspecDTO[UpdateUserData]):
    config = DTOConfig(partial=True, rename_strategy="camel")
