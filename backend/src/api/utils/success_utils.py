from typing import Any
from backend.src.api.responses import SuccessResponse
from backend.src.api.dto.auth_dto import UserResponse, TokenInfo


def create_success(
    message: str,
    data: dict[str, Any] | None = None,
) -> SuccessResponse:
    return SuccessResponse(
        message=message,
        data=data or {},
    )


def login_success(token_info: TokenInfo) -> SuccessResponse:
    return create_success(
        message="Login successful",
        data={
            "access": token_info.access,
            "refresh": token_info.refresh,
            "token_type": token_info.token_type,
        },
    )


def logout_success(message: str = "Successfully logged out") -> SuccessResponse:
    return create_success(message=message)


def refresh_success(access_token: str, token_type: str = "Bearer") -> SuccessResponse:
    return create_success(
        message="Token refreshed successfully",
        data={
            "access": access_token,
            "token_type": token_type,
        },
    )


def password_change_success(message: str = "Password changed successfully") -> SuccessResponse:
    return create_success(message=message)


def user_registration_success(user: UserResponse) -> SuccessResponse:
    return create_success(
        message="User registered successfully",
        data={
            "user": {
                "name": user.name,
                "email": user.email,
                "user_id": user.id,
                "is_active": user.is_active,
                "is_verified": user.is_verify,
            }
        },
    )


def user_profile_success(user: UserResponse) -> SuccessResponse:
    return create_success(
        message="User profile retrieved",
        data={
            "user": {
                "name": user.name,
                "email": user.email,
                "user_id": user.id,
                "is_active": user.is_active,
                "is_verified": user.is_verify,
            }
        },
    )
