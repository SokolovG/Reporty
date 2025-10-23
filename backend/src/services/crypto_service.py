from backend.src.database.repositories.ai_repository import AIProviderKeyRepository


class CryptoService:
    def __init__(self, api_key_repo: AIProviderKeyRepository):
        self.api_key_repo = api_key_repo

    # TODO: maybe vault docker
    def encrypt(self, data: str) -> str:
        return ""

    def decrypt(self, encrypted_data: str) -> str:
        return ""
