from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.core.exception import global_exception_handler, validation_exception_handler, value_error_handler
from app.core.database import init_sqlalchemy_db, close_sqlalchemy_db
from app.api.v1 import api_router as api_v1_router
# MongoDB connection
# MONGO_URI = os.getenv("MONGO_URI")
# client = AsyncIOMotorClient(MONGO_URI)
# db = client.get_default_database()

# FastAPI app
app = FastAPI(title="Resume Job Finder API")

# Startup and shutdown events
async def startup_handler():
    # await connect_to_mongo()
    await init_sqlalchemy_db()
    pass


async def shutdown_handler():
    # await close_mongo_connection()
    await close_sqlalchemy_db()
    pass


app.add_event_handler("startup", startup_handler)
app.add_event_handler("shutdown", shutdown_handler)


app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Register API routers
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hello from resume-job-finder!"}

