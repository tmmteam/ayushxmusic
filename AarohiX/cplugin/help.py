from typing import Union

from pyrogram import filters, types, Client
from pyrogram.types import InlineKeyboardMarkup, Message

from AarohiX import app
from AarohiX.utils import first_page, second_page
from AarohiX.utils.database import get_lang
from AarohiX.utils.decorators.language import LanguageStart, languageCB
from AarohiX.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, HELP_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers
from AarohiX.misc import SUDOERS
from time import time
import asyncio
from AarohiX.utils.extraction import extract_user
from AarohiX.utils.database.clonedb import (
    get_owner_id_from_db,
    get_cloned_support_chat,
    get_cloned_support_channel,
)

# Spam protection
user_last_message_time = {}
user_command_count = {}
SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5


@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    bot = await client.get_me()
    C_BOT_SUPPORT_CHAT = await get_cloned_support_chat(bot.id)
    C_SUPPORT_CHAT = f"https://t.me/{C_BOT_SUPPORT_CHAT}"
    C_BOT_SUPPORT_CHANNEL = await get_cloned_support_channel(bot.id)
    C_SUPPORT_CHANNEL = f"https://t.me/{C_BOT_SUPPORT_CHANNEL}"

    is_callback = isinstance(update, types.CallbackQuery)
    chat_id = update.message.chat.id if is_callback else update.chat.id
    language = await get_lang(chat_id)
    _ = get_string(language)
    keyboard = first_page(_)

    if is_callback:
        try:
            await update.answer()
            await update.edit_message_text(
                _["help_1"].format(C_SUPPORT_CHAT), reply_markup=keyboard
            )
        except:
            pass
    else:
        try:
            await update.delete()
        except:
            pass
        await update.reply_photo(
            photo=HELP_IMG_URL,
            caption=_["help_1"].format(C_SUPPORT_CHAT),
            reply_markup=keyboard,
        )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    user_id = message.from_user.id
    current_time = time()

    last_message_time = user_last_message_time.get(user_id, 0)
    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            hu = await message.reply_text(
                f"**{message.from_user.mention} ᴘʟᴇᴀsᴇ ᴅᴏɴᴛ ᴅᴏ sᴘᴀᴍ, ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 sᴇᴄ**"
            )
            await asyncio.sleep(3)
            await hu.delete()
            return
    else:
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)

    if cb == "hb9":
        if CallbackQuery.from_user.id not in SUDOERS:
            return await CallbackQuery.answer(
                "😎 Pehle OWNER ka loda lo jake 😆😆", show_alert=True
            )
        await CallbackQuery.edit_message_text(helpers.HELP_9, reply_markup=keyboard)
        return await CallbackQuery.answer()

    try:
        await CallbackQuery.answer()
    except:
        pass

    help_map = {
        "hb1": helpers.HELP_1,
        "hb2": helpers.HELP_2,
        "hb3": helpers.HELP_3,
        "hb4": helpers.HELP_4,
        "hb5": helpers.HELP_5,
        "hb6": helpers.HELP_6,
        "hb7": helpers.HELP_7,
        "hb8": helpers.HELP_8,
        "hb10": helpers.HELP_10,
        "hb11": helpers.HELP_11,
        "hb12": helpers.HELP_12,
        "hb13": helpers.HELP_13,
        "hb14": helpers.HELP_14,
        "hb15": helpers.HELP_15,
        "chelp": helpers.CLONE_HELP_2,
        "cloghelp": helpers.CLONE_LOGGER_HELP,
    }

    if cb in help_map:
        await CallbackQuery.edit_message_text(help_map[cb], reply_markup=keyboard)


@app.on_callback_query(filters.regex("dilXaditi") & ~BANNED_USERS)
@languageCB
async def first_pagexx(client, CallbackQuery, _):
    menu_next = second_page(_)
    try:
        await CallbackQuery.message.edit_text(_["help_1"], reply_markup=menu_next)
    except:
        pass
