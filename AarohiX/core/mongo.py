import motor.motor_asyncio
from pymongo import MongoClient
import os

# Heroku config var se Mongo URI lena
MONGO_DB_URI = os.environ.get("MONGO_DB_URI")

if not MONGO_DB_URI:
    raise Exception("❌ MONGO_DB_URI not found in environment variables!")

# Motor client for async access (for await calls)
motor_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI)
mongodb = motor_client.get_default_database()

# PyMongo client for normal access (non-await)
pymongo_client = MongoClient(MONGO_DB_URI)
pymongodb = pymongo_client.get_default_database()
