from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from app.db.mongodb import connect_to_mongo, close_mongo_connection

# Load environment variables
load_dotenv()

# MongoDB connection
# MONGO_URI = os.getenv("MONGO_URI")
# client = AsyncIOMotorClient(MONGO_URI)
# db = client.get_default_database()

# FastAPI app
app = FastAPI(title="Resume Job Finder API")

# Startup and shutdown events
async def startup_handler():
    await connect_to_mongo()


async def shutdown_handler():
    await close_mongo_connection()


app.add_event_handler("startup", startup_handler)
app.add_event_handler("shutdown", shutdown_handler)

@app.get("/")
async def root():
    return {"message": "Hello from resume-job-finder!"}

# @app.get("/test-mongo")
# async def test_mongo():
#     try:
#         # This will fetch first document from a test collection
#         doc = await db.test_collection.find_one()
#         return {"status": "connected", "first_doc": doc}
#     except Exception as e:
#         return {"status": "error", "detail": str(e)}


