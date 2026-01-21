from pydantic.dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    email: str
    is_active: bool
    is_verify: bool
    display_name: str | None = None
    department: str | None = None
    position: str | None = None
    ai_auto_process: bool = False
    ai_provider_id: int | None = None

    def activate(self) -> None:
        """Activate user account."""
        if self.is_active:
            raise ValueError("User already active")
        self.is_active = True

    def verify_email(self) -> None:
        """Mark email as verified."""
        if self.is_verify:
            raise ValueError("Email already verified")
        self.is_verify = True

    def can_use_ai(self) -> bool:
        """Check if user can use AI features."""
        return self.is_active and self.ai_provider_id is not None
