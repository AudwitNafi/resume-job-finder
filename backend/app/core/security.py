"""
Security Utility Module

This module handles:
- JWT token creation & verification (access, refresh, password reset)
- Password hashing & verification
"""

from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.core.logger import logger
from fastapi import Depends, HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# ----------------------
# Password Hashing Setup
# ----------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain password for storing in DB."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)


# ----------------------
# JWT Token Utilities
# ----------------------
def create_access_token(user_id: str):
    """Create a JWT access token for a user."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"sub": user_id, "type": "access", "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt, int(expire.timestamp())


def create_refresh_token(user_id: str):
    """Create a JWT refresh token for a user."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"sub": user_id, "type": "refresh", "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt, int(expire.timestamp())


def verify_token(token: str) -> str:
    """Verify a JWT token and return its subject."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        raise
    except jwt.InvalidTokenError:
        logger.error("Token is invalid")
        raise


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """Extract user_id from JWT token using OAuth2 scheme."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        logger.error("Token is invalid")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
