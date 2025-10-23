from typing import Optional
from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.services.interface.auth_service_interface import UserServiceInterface
from app.repository.user_repository_sql import UserRepository
from app.schemas.user_dto import UserCreate, UserResponse, TokenResponse
from app.models.user_sql import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.core.logger import logger


class UserService(UserServiceInterface):
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, dto: UserCreate) -> UserResponse:
        """
        Create a new user in the database.
        """
        # Check if email or username already exists
        existing_user = await self.user_repo.get_by_email(dto.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        existing_username = await self.user_repo.get_by_username(dto.username)
        if existing_username:
            raise ValueError("User with this username already exists")

        # Hash the password
        hashed_password = hash_password(dto.password)

        # Create new user object
        user = User(
            username=dto.username,
            email=dto.email,
            hashed_password=hashed_password,
            is_active=True,
            is_admin=False,
            created_at=datetime.now(timezone.utc),
            last_login=datetime.now(timezone.utc),
        )

        # Save to DB
        created_user = await self.user_repo.create(user)

        return UserResponse.model_validate(created_user)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Verify user credentials and return the User if valid.
        """
        user = await self.user_repo.get_by_email(email)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        # Update last login timestamp
        user.last_login = datetime.now(timezone.utc)
        await self.user_repo.update_last_login(user)

        return user

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        return await self.user_repo.get_by_id(user_id)

    async def login_user(self, email: str, password: str) -> TokenResponse:
        """
        Authenticate and return JWT tokens (access + refresh).
        """
        user = await self.authenticate_user(email, password)
        logger.info(f"Trying login for {email}")

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token, access_exp = create_access_token(str(user.id))
        refresh_token, _ = create_refresh_token(str(user.id))

        return TokenResponse.model_validate(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": access_exp,
                "token_type": "bearer",
            }
        )
        
    async def get_current_user(self, user_id: str) -> UserResponse:
        try:
            user_id_int = int(user_id)
            
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID",
            )

        user: Optional[User] = await self.user_repo.get_by_id(user_id_int)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserResponse.model_validate(user)

