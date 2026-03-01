import re

from backend.src.infrastructure.exceptions.api_exceptions import ValidationError


class PasswordValidator:
    """Password strength validator."""

    MIN_LENGTH = 8

    @classmethod
    def validate(cls, password: str) -> None:
        """Validate password strength.

        Raises:
            ValidationError: If password doesn't meet requirements
        """
        if len(password) < cls.MIN_LENGTH:
            raise ValidationError(
                f"Password must be at least {cls.MIN_LENGTH} characters",
                details={"field": "password", "min_length": cls.MIN_LENGTH},
            )

        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                "Password must contain at least one uppercase letter",
                details={"field": "password", "requirement": "uppercase"},
            )

        if not re.search(r"[a-z]", password):
            raise ValidationError(
                "Password must contain at least one lowercase letter",
                details={"field": "password", "requirement": "lowercase"},
            )

        if not re.search(r"\d", password):
            raise ValidationError(
                "Password must contain at least one digit",
                details={"field": "password", "requirement": "digit"},
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError(
                "Password must contain at least one special character",
                details={"field": "password", "requirement": "special_char"},
            )


class EmailValidator:
    """Email validation."""

    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    @classmethod
    def validate(cls, email: str) -> None:
        """Validate email format.

        Raises:
            ValidationError: If email format is invalid
        """
        if not cls.EMAIL_REGEX.match(email):
            raise ValidationError("Invalid email format", details={"field": "email"})
