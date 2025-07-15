from pyrogram import filters, Client
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import Message
from time import time
import asyncio

from config import BANNED_USERS
from AarohiX import app
from AarohiX.utils.database import set_cmode
from AarohiX.utils.decorators.admins import AdminActual

# Anti-spam tracking
user_last_message_time = {}
user_command_count = {}
SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5


@app.on_message(filters.command("channelplay") & filters.group & ~BANNED_USERS)
@AdminActual
async def playmode_handler(client: Client, message: Message, _):
    user_id = message.from_user.id
    current_time = time()

    last_time = user_last_message_time.get(user_id, 0)
    if current_time - last_time < SPAM_WINDOW_SECONDS:
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            warn = await message.reply_text(
                f"**{message.from_user.mention}, ᴘʟᴇᴀsᴇ ᴀᴠᴏɪᴅ sᴘᴀᴍᴍɪɴɢ. ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 sᴇᴄᴏɴᴅs.**"
            )
            await asyncio.sleep(3)
            return await warn.delete()
    else:
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    if len(message.command) < 2:
        return await message.reply_text(_["cplay_1"].format(message.chat.title))

    query = message.text.split(None, 2)[1].lower().strip()
    if query == "disable":
        await set_cmode(message.chat.id, None)
        return await message.reply_text(_["cplay_7"])

    elif query == "linked":
        chat = await client.get_chat(message.chat.id)
        if chat.linked_chat:
            chat_id = chat.linked_chat.id
            await set_cmode(message.chat.id, chat_id)
            return await message.reply_text(
                _["cplay_3"].format(chat.linked_chat.title, chat_id)
            )
        else:
            return await message.reply_text(_["cplay_2"])

    else:
        try:
            chat = await client.get_chat(query)
        except:
            return await message.reply_text(_["cplay_4"])

        if chat.type != ChatType.CHANNEL:
            return await message.reply_text(_["cplay_5"])

        try:
            async for user in client.get_chat_members(chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
                if user.status == ChatMemberStatus.OWNER:
                    cusn = user.user.username
                    crid = user.user.id
        except:
            return await message.reply_text(_["cplay_4"])

        if crid != message.from_user.id:
            return await message.reply_text(_["cplay_6"].format(chat.title, cusn))

        await set_cmode(message.chat.id, chat.id)
        return await message.reply_text(_["cplay_3"].format(chat.title, chat.id))
