from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import secrets


# Adjust the path if needed (relative to env.py location)
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

class Settings(BaseSettings):
    # Project
    DOMAIN: str = "localhost"
    FRONTEND_HOST: str = "http://localhost:3000"
    ENVIRONMENT: str = "local"  # local, staging, production
    PROJECT_NAME: str = "Full Stack FastAPI Project"
    STACK_NAME: str = "full-stack-fastapi-project"

    # Backend
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "https://localhost",
        "https://localhost:3000",
        "http://localhost.tiangolo.com",
    ]
    SECRET_KEY: str = secrets.token_urlsafe(32)
    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "changethis"

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "app"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "changethis"
    
    #MongoDB
    MONGO_URI: str = "mongodb+srv://..."  

    MONGO_DB: str = "resume_job_finder"

    # Docker images
    DOCKER_IMAGE_BACKEND: str = "backend"
    DOCKER_IMAGE_FRONTEND: str = "frontend"


    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    class Config:
        env_file = ".env"  # Automatically load values from .env file


settings = Settings()

if __name__ == "__main__":
    print(settings.DATABASE_URL)