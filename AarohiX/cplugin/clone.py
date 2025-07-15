import time
import random
from datetime import datetime

import psutil
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from AarohiX import app
from config import PING_IMG_URL, STREAMI_PICS
from AarohiX.utils import get_readable_time
from AarohiX.utils.decorators.language import language

APP_LINK = "https://t.me/falcon_musis_roBot"  # update your cloned bot URL here


@app.on_message(filters.command("clone"))
@language
async def ping_clone(client: Client, message: Message, _):
    bot = await client.get_me()

    await message.reply_photo(
        photo=random.choice(STREAMI_PICS),
        caption=_["NO_CLONE_MSG"],
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Cʟᴏɴᴇ Bᴏᴛ", url=APP_LINK)]
            ]
        )
    )
