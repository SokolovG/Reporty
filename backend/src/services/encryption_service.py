from cryptography.fernet import Fernet
from logging import getLogger
from backend.src.core.settings import settings


logger = getLogger(__name__)


class EncryptionService:
    """Service for encrypting/decrypting sensitive data."""

    def __init__(self) -> None:
        self.master_key = settings.MASTER_ENCRYPTION_KEY
        if not self.master_key:
            raise ValueError(
                "MASTER_ENCRYPTION_KEY not found in environment. "
                "Generate one with: Fernet.generate_key()"
            )

        try:
            self.fernet = Fernet(self.master_key)
        except Exception as e:
            logger.error(f"Failed to initialize encryption: {e}")
            raise

    async def encrypt(self, plain_text: str) -> str:
        """
        Encrypt plain text string.

        Args:
            plain_text: Text to encrypt (e.g., API key)

        Returns:
            Encrypted bytes

        Raises:
            ValueError: If plain_text is empty
            Exception: If encryption fails
        """
        if not plain_text:
            raise ValueError("Cannot encrypt empty string")

        try:
            encrypted = self.fernet.encrypt(plain_text.encode())
            logger.debug("Successfully encrypted data")
            return encrypted
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    async def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt encrypted bytes back to string.

        Args:
            encrypted_data: Encrypted bytes

        Returns:
            Decrypted plain text string

        Raises:
            Exception: If decryption fails (wrong key, corrupted data)
        """
        try:
            decrypted = self.fernet.decrypt(encrypted_data)
            logger.debug("Successfully decrypted data")
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise
