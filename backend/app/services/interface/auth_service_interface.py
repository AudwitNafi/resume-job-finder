from __future__ import annotations
from typing import Optional
from app.schemas.user_dto import UserCreate, UserResponse
from abc import ABC, abstractmethod


class UserServiceInterface(ABC):
    @abstractmethod
    async def create_user(self, dto: UserCreate) -> UserResponse:
        raise NotImplementedError

    @abstractmethod
    async def authenticate_user(
        self, username_or_email: str, password: str
    ) -> Optional[UserResponse]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        raise NotImplementedError

    @abstractmethod
    async def login_user(self, email: str, password: str) -> Optional[dict]:
        raise NotImplementedError
