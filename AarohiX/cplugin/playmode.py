from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, Message

from AarohiX import app
from AarohiX.utils.database import get_playmode, get_playtype, is_nonadmin_chat
from AarohiX.utils.decorators import language
from AarohiX.utils.inline.settings import playmode_users_markup
from config import BANNED_USERS


@Client.on_message(
    filters.command(
        ["playmode", "mode"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]
    )
    & filters.group
    & ~BANNED_USERS
)
@language
async def playmode_(client, message: Message, _):
    playmode = await get_playmode(message.chat.id)
    if playmode == "Direct":
        Direct = True
    else:
        Direct = None
    is_non_admin = await is_nonadmin_chat(message.chat.id)
    if not is_non_admin:
        Group = True
    else:
        Group = None
    playty = await get_playtype(message.chat.id)
    if playty == "Everyone":
        Playtype = None
    else:
        Playtype = True
    buttons = playmode_users_markup(_, Direct, Group, Playtype)
    response = await message.reply_text(
        _["play_22"].format(message.chat.title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )
