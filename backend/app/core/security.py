from fastapi import Header, HTTPException, status

from app.core.config import settings


def verify_admin_token(authorization: str | None = Header(default=None)) -> None:
    expected = f"Bearer {settings.admin_token}"
    if authorization != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
