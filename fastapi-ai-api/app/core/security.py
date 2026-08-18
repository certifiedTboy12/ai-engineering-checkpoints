import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from uuid import UUID
from typing import Any, cast
from app.config.constant import JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ACCESS_TOKEN_SECRET


def create_access_token(user_id: UUID) -> str:
    """
    Generate a JWT access token for a user.
    """

    expire_minutes = JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    if expire_minutes is None:
        raise ValueError("JWT_ACCESS_TOKEN_EXPIRE_MINUTES is not configured")

    expire = datetime.now(timezone.utc) + timedelta(minutes=float(expire_minutes))

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    token: str = cast(Any, jwt).encode(
        payload,
        JWT_ACCESS_TOKEN_SECRET,
        algorithm=JWT_ALGORITHM,
    )

    return token


def verify_access_token(token: str) -> str:
    """
    Verify a JWT and return the user ID.
    """

    try:
        payload: dict[str, Any] = cast(Any, jwt).decode(
            token,
            JWT_ACCESS_TOKEN_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise InvalidTokenError("Token has no user ID")

        return user_id

    except (InvalidTokenError, ValueError):
        raise