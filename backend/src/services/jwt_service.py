from datetime import datetime, timedelta

import bcrypt
import jwt

from backend.src.api.dto import TokenInfo
from backend.src.core.settings import settings


class JWTService:
    async def create_access_token(self, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=15),
            "type": "access",
        }

        with open(settings.private_key, "rb") as key_file:
            pv_key = key_file.read()
        token: str = jwt.encode(payload=payload, key=pv_key, algorithm=settings.algorithm)
        return token

    async def verify_token(self, token: str) -> dict | None:
        try:
            with open(settings.public_key, "rb") as key_file:
                public_key = key_file.read()

            payload: dict = jwt.decode(token, public_key, algorithms=[settings.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    async def create_refresh_token(self, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=7),
            "type": "refresh",
        }

        with open(settings.private_key, "rb") as key_file:
            pv_key = key_file.read()
        token: str = jwt.encode(payload=payload, key=pv_key, algorithm=settings.algorithm)
        return token

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

    async def login(self, user_id: int) -> TokenInfo:
        access = await self.create_access_token(user_id)
        refresh = await self.create_refresh_token(user_id)
        return TokenInfo(refresh=refresh, access=access, token_type="Bearer")
