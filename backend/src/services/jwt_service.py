from typing import NamedTuple

import bcrypt


class Tokens(NamedTuple):
    access: str
    refresh: str


class JWTService:
    async def create_access_token(self, user_id: int) -> None: ...
    async def verify_token(self, token: str) -> dict | None: ...
    def hash_password(self, password: str) -> str:
        bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(bytes, salt)
        hash = hash_bytes.decode("utf-8")
        return hash

    async def verify_password(self, password: str, hash_password: str) -> bool:
        password_bytes = password.encode("utf-8")
        hash_bytes = hash_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hash_bytes)

    async def login(self) -> Tokens:
        return Tokens(
            access="",
            refresh="",
        )
