from fastapi import APIRouter, Depends, status
from app.schemas.user_dto import UserCreate, UserResponse, TokenResponse, UserLogin
from app.services.interface.auth_service_interface import UserServiceInterface
from app.core.dependency import get_user_service
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import get_current_user_id

# from app.core.security import create_access_token

from typing import Annotated
from fastapi import Body



router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(
    request: Annotated[
        UserCreate,
        Body(
            openapi_examples={
                "john_doe": {
                    "summary": "A normal user signup",
                    "description": "A **normal** user signup works correctly.",
                    "value": {
                        "username": "john_doe",
                        "email": "john_doe@example.com",
                        "password": "strongpassword123",
                    },
                },
                "jane_smith": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert numeric `strings` to actual `numbers` automatically if needed",
                    "value": {
                        "username": "jane_smith",
                        "email": "jane_smith@example.com",
                        "password": "anotherpassword456",
                    },
                },
            },
        ),
    ],
    user_service: UserServiceInterface = Depends(get_user_service),
):

    return await user_service.create_user(request)


@router.post("/login/json", response_model=TokenResponse)
async def login_json(request: UserLogin, user_service: UserServiceInterface = Depends(get_user_service)):
    return await user_service.login_user(request.email, request.password)


@router.post("/login", response_model=TokenResponse)
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), user_service: UserServiceInterface = Depends(get_user_service)):
    return await user_service.login_user(form_data.username, form_data.password)

@router.get("/me", response_model=UserResponse)
async def get_me(
    user_id: int = Depends(get_current_user_id),
    user_service: UserServiceInterface = Depends(get_user_service),
):
    return await user_service.get_current_user(user_id)
