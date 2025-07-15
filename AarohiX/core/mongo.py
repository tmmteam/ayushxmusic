from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from pyrogram import Client

import config
from ..logging import LOGGER

TEMP_MONGODB = ""

if not config.MONGO_DB_URI:
    LOGGER(__name__).warning("No MONGO DB URL found. LOL")
    
    temp_client = Client(
        "Anon",
        bot_token=config.BOT_TOKEN,
        api_id=config.API_ID,
        api_hash=config.API_HASH,
    )
    temp_client.start()
    info = temp_client.get_me()
    username = info.username
    temp_client.stop()
    
    _mongo_async_ = _mongo_client_(TEMP_MONGODB)
    _mongo_sync_ = MongoClient(TEMP_MONGODB)
    
    mongodb = _mongo_async_[username]
    pymongodb = _mongo_sync_[username]
else:
    _mongo_async_ = _mongo_client_(config.MONGO_DB_URI)
    _mongo_sync_ = MongoClient(config.MONGO_DB_URI)
    
    # 👇👇 Use the correct database name here instead of "Anon"
    mongodb = _mongo_async_.get_default_database()
    pymongodb = _mongo_sync_.get_default_database()
