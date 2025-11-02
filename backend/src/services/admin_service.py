from litestar import Request
from sqladmin.authentication import AuthenticationBackend


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str): ...

    async def login(self, request: Request) -> bool: ...

    async def authenticate(self, request: Request) -> bool:
        ...
        # JWT validation
