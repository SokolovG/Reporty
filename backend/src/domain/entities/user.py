from dataclasses import dataclass

from backend.src.domain.exceptions.domain_exceptions import (
    EmailAlreadyVerifiedError,
    UserAlreadyActiveError,
)


@dataclass
class User:
    """Domain entity representing a user"""

    id: int
    name: str
    email: str

    # Status
    is_active: bool = False
    is_verify: bool = False
    is_admin: bool = False

    # Profile
    display_name: str | None = None
    department: str | None = None
    position: str | None = None

    # AI settings
    ai_auto_process: bool = False
    ai_provider_id: int | None = None
    ai_model_id: int | None = None
    # External systems
    external_system_id: int | None = None

    @property
    def have_external_system(self) -> bool:
        """Check if user has an external system configured"""
        return self.external_system_id is not None

    def activate(self) -> None:
        """Activate user account

        Business rule: Cannot activate already active user
        """
        if self.is_active:
            raise UserAlreadyActiveError(f"User {self.id} is already active")
        self.is_active = True

    def deactivate(self) -> None:
        """Deactivate user account"""
        self.is_active = False

    def verify_email(self) -> None:
        """Mark email as verified

        Business rule: Cannot verify already verified email
        """
        if self.is_verify:
            raise EmailAlreadyVerifiedError(f"Email for user {self.id} is already verified")
        self.is_verify = True

    def can_use_ai(self) -> bool:
        """Check if user can use AI features

        Business rule: User must be active and have AI provider configured
        """
        return self.is_active and self.ai_provider_id is not None

    def configure_ai(
        self,
        provider_id: int,
        model_id: int | None = None,
        auto_process: bool = False,
        custom_prompt: str | None = None,
    ) -> None:
        """Configure AI settings for user"""
        self.ai_provider_id = provider_id
        self.ai_model_id = model_id
        self.ai_auto_process = auto_process
        self.custom_prompt = custom_prompt

    def update_profile(
        self,
        display_name: str | None = None,
        department: str | None = None,
        position: str | None = None,
    ) -> None:
        """Update user profile information"""
        if display_name is not None:
            self.display_name = display_name
        if department is not None:
            self.department = department
        if position is not None:
            self.position = position
