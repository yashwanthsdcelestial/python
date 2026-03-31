from fastapi import Depends, Header
from typing import Optional
from exceptions.custom_exceptions import ForbiddenError, InvalidCredentialsError
from utils.session_store import get_session


def get_current_user(x_auth_token: Optional[str] = Header(default=None)) -> dict:
    """Read X-Auth-Token header and return the session user dict."""
    if not x_auth_token:
        raise InvalidCredentialsError("Not authenticated. Please log in first.")
    user = get_session(x_auth_token)
    if not user:
        raise InvalidCredentialsError("Invalid or expired token. Please log in again.")
    return user


def require_role(role: str):
    """FastAPI dependency that enforces a specific role."""
    def dependency(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("role") != role:
            raise ForbiddenError(
                f"Access denied. Requires role '{role}', "
                f"but your role is '{current_user.get('role')}'."
            )
        return current_user
    return dependency