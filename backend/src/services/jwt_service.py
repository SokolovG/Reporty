import bcrypt


class JWTService:
    def create_access_token(self, user_id: int) -> str: ...
    def verify_token(self, token: str) -> dict | None: ...
    def hash_password(self, password: str) -> str:
        bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(bytes, salt)
        hash = hash_bytes.decode("utf-8")
        return hash
