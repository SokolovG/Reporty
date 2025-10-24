from datetime import datetime, timedelta

import bcrypt
import jwt

from backend.src.api.dto import TokenInfo
from backend.src.core.exceptions import AuthenticationError
from backend.src.core.settings import settings


class JWTService:
    async def create_access_token(self, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=15),
            "type": "access",
        }

        with open(settings.PRIVATE_KEY, "rb") as key_file:
            pv_key = key_file.read()
        token: str = jwt.encode(payload=payload, key=pv_key, algorithm=settings.ALHOTIRHM)
        return token

    async def verify_token(self, token: str, expected_type: str = "access") -> dict:
        try:
            with open(settings.PUBLIC_KEY, "rb") as key_file:
                public_key = key_file.read()

            payload: dict = jwt.decode(token, public_key, algorithms=[settings.ALHOTIRHM])
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
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=7),
            "type": "refresh",
        }

        with open(settings.PRIVATE_KEY, "rb") as key_file:
            pv_key = key_file.read()
        token: str = jwt.encode(payload=payload, key=pv_key, algorithm=settings.ALHOTIRHM)
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
