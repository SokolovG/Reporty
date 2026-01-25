from dataclasses import dataclass

from backend.src.domain.exceptions import (
    EmailAlreadyVerifiedError,
    UserAlreadyActiveError,
    UserCannotUseAIError,
    UserNotActiveError,
)


@dataclass
class User:
    """Domain entity representing a user.

    Business Rules:
    - Active users cannot be activated again
    - Verified emails cannot be verified again
    - Users must be active and have AI provider configured to use AI
    """

    id: int
    name: str
    email: str
    password_hash: str

    is_active: bool = False
    is_verify: bool = False
    is_admin: bool = False

    display_name: str | None = None
    department: str | None = None
    position: str | None = None

    ai_auto_process: bool = False
    ai_provider_id: int | None = None
    ai_model_id: int | None = None
    custom_prompt: str | None = None
    external_system_id: int | None = None

    def activate(self) -> None:
        """Activate user account.

        Business Rule: Cannot activate already active user.

        Raises:
            UserAlreadyActiveError: If user is already active
        """
        if self.is_active:
            raise UserAlreadyActiveError(self.id)

        self.is_active = True

    @property
    def have_external_system(self) -> bool:
        """Check if user has external system configured."""
        return self.external_system_id is not None

    def deactivate(self) -> None:
        """Deactivate user account.

        Deactivated users cannot perform most actions in the system.
        """
        self.is_active = False

    def verify_email(self) -> None:
        """Mark email as verified.

        Business Rule: Cannot verify already verified email.

        Raises:
            EmailAlreadyVerifiedError: If email is already verified
        """
        if self.is_verify:
            raise EmailAlreadyVerifiedError(self.id, self.email)

        self.is_verify = True

    def can_use_ai(self) -> bool:
        """Check if user can use AI features.

        Business Rule: User must be active and have AI provider configured.

        Returns:
            True if user can use AI, False otherwise
        """
        return self.is_active and self.ai_provider_id is not None

    def ensure_can_use_ai(self) -> None:
        """Ensure user can use AI features.

        Raises:
            UserNotActiveError: If user is not active
            UserCannotUseAIError: If user doesn't have AI provider configured
        """
        if not self.is_active:
            raise UserNotActiveError(self.id)

        if self.ai_provider_id is None:
            raise UserCannotUseAIError(
                self.id, "AI provider not configured. Please configure AI settings first."
            )

    def configure_ai(
        self,
        provider_id: int | None = None,
        model_id: int | None = None,
        auto_process: bool | None = None,
        custom_prompt: str | None = None,
    ) -> None:
        """Configure AI settings for user.

        Args:
            provider_id: ID of the AI provider to use
            model_id: Optional ID of specific AI model
            auto_process: Whether to automatically process records with AI
            custom_prompt: Optional custom system prompt for AI
        """
        if provider_id is not None:
            self.ai_provider_id = provider_id

        if model_id is not None:
            self.ai_model_id = model_id

        if auto_process is not None:
            self.ai_auto_process = auto_process

        if custom_prompt is not None:
            self.custom_prompt = custom_prompt

    def disable_ai(self) -> None:
        """Disable AI features for user."""
        self.ai_provider_id = None
        self.ai_model_id = None
        self.ai_auto_process = False

    def update_profile(
        self,
        display_name: str | None = None,
        department: str | None = None,
        position: str | None = None,
    ) -> None:
        """Update user profile information.

        Args:
            display_name: User's display name
            department: User's department
            position: User's position/role
        """
        if display_name is not None:
            self.display_name = display_name

        if department is not None:
            self.department = department

        if position is not None:
            self.position = position

    def make_admin(self) -> None:
        """Grant admin privileges to user."""
        self.is_admin = True

    def revoke_admin(self) -> None:
        """Revoke admin privileges from user."""
        self.is_admin = False
