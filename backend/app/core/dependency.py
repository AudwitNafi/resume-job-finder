from fastapi import Depends
from app.repository.user_repository_sql import UserRepository
from app.services.auth_service import UserService
from app.services.interface.auth_service_interface import UserServiceInterface
from app.core.database import get_db, AsyncSession



# Factory-like dependency creators



def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session=session)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserServiceInterface:
    return UserService(user_repo)