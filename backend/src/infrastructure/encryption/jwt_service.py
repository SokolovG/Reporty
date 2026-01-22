from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from backend.src.application.dto.auth import TokenInfo
from backend.src.infrastructure.config.settings import settings
from backend.src.infrastructure.exceptions.api_exceptions import AuthenticationError


class JWTService:
    async def create_access_token(self, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
            "type": "access",
        }

        token: str = jwt.encode(
            payload=payload, key=settings.JWT_PRIVATE_KEY, algorithm=settings.ALGORITHM
        )
        return token

    async def verify_token(self, token: str, expected_type: str = "access") -> dict:
        try:
            payload: dict = jwt.decode(
                token, settings.JWT_PUBLIC_KEY, algorithms=[settings.ALGORITHM]
            )
            token_type = payload.get("type")
            if token_type != expected_type:
                raise AuthenticationError(
                    "Token type != access!", details={"token_type": token_type}
                )
            return payload
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise AuthenticationError("Expired Signature Error or Invalid Token Error")

    async def create_refresh_token(self, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
            "type": "refresh",
        }

        token: str = jwt.encode(
            payload=payload, key=settings.JWT_PRIVATE_KEY, algorithm=settings.ALGORITHM
        )
        return token

    def hash_password(self, password: str) -> str:
        bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(bytes, salt)
        hash: str = hash_bytes.decode("utf-8")
        return hash

    async def verify_password(self, password: str, hash_password: str) -> bool:
        password_bytes = password.encode("utf-8")
        hash_bytes = hash_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hash_bytes)

    async def login(self, user_id: int) -> TokenInfo:
        access = await self.create_access_token(user_id)
        refresh = await self.create_refresh_token(user_id)
        return TokenInfo(refresh=refresh, access=access, token_type="Bearer")
