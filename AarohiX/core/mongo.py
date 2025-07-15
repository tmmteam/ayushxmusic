import motor.motor_asyncio
from pymongo import MongoClient
import os

# Mongo URI from env
MONGO_DB_URI = os.getenv("MONGO_DB_URI", None)

if not MONGO_DB_URI:
    raise Exception("MONGO_DB_URI not found in environment.")

# Async MongoDB client (for async/await usage)
motor_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI)
mongodb = motor_client["aarohixdb"]

# Sync MongoDB client (for sync methods like find_one, etc.)
pymongo_client = MongoClient(MONGO_DB_URI)
pymongodb = pymongo_client["aarohixdb"]
