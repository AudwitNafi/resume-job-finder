from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Base class for models
Base = declarative_base()

# Ensure async driver is used at runtime
ASYNC_DATABASE_URL = settings.DATABASE_URL
if not ASYNC_DATABASE_URL.startswith("postgresql+asyncpg://"):
    ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,
    future=True
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Dependency for FastAPI routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# Initialize the DB (used on startup)
async def init_sqlalchemy_db():
    """
    Initialize the database connection and create tables if needed.
    This is called once during FastAPI startup.
    """
    async with engine.begin() as conn:
        # Import all models here to register them with Base.metadata
        # from app.model import user, chat  # example imports
        await conn.run_sync(Base.metadata.create_all)


# Graceful shutdown
async def close_sqlalchemy_db():
    """
    Close the SQLAlchemy engine connection.
    Called during FastAPI shutdown.
    """
    await engine.dispose()
