from backend.src.api.dto import (
    RefreshTokenRequest,
    ChangePasswordRequest,
    LogoutRequest,
    LoginRequest,
    RegisterRequest,
)
from backend.src.database.repositories import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.repo = user_repository

    async def register(self, data: RegisterRequest) -> None:
        pass

    async def login(self, data: LoginRequest) -> None:
        pass

    async def logout(self, data: LogoutRequest) -> None:
        pass

    async def refresh(self, data: RefreshTokenRequest) -> None:
        pass

    async def change_password(self, data: ChangePasswordRequest) -> None:
        pass

    async def get_me(self) -> None:
        pass
