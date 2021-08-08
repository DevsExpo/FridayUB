# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import logging

from pyrogram import filters

from database.autopostingdb import (
    add_new_autopost,
    check_if_autopost_in_db,
    del_autopost,
    get_autopost,
)
from main_startup.core.decorators import friday_on_cmd, listen
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@friday_on_cmd(
    ["autopost"],
    cmd_help={
        "help": "Add Channel To AutoPost List!",
        "example": "{ch}autopost @fridaysupportofficial",
    },
    chnnl_only=True,
)
async def autopost(client, message):
    engine = message.Engine
    mess_age_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    chnnl = get_text(message)
    if not chnnl:
        await mess_age_.edit(engine.get_string("INPUT_REQ").format("Chat ID"))
        return
    try: 
        channel_str = int(chnnl)
    except ValueError:
        channel_str = str(chnnl)
    try:
        u_ = await client.get_chat(channel_str)
    except:
        await mess_age_.edit(engine.get_string("INVALID_CHAT_ID"))
        return
    channel_str = int(u_.id)
    if await check_if_autopost_in_db(int(message.chat.id), channel_str):
        await mess_age_.edit(engine.get_string("CHAT_ALREADY_IN_DB"))
        return
    await add_new_autopost(int(message.chat.id), channel_str)
    await mess_age_.edit(engine.get_string("AUTOPOSTING_1").format(chnnl))


@friday_on_cmd(
    ["rmautopost"],
    cmd_help={
        "help": "Remove A Channel From Autopost List",
        "example": "{ch}rmautopost @fridaysupportofficial",
    },
    chnnl_only=True,
)
async def rmautopost(client, message):
    engine = message.Engine
    mess_age_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    chnnl = get_text(message)
    if not chnnl:
        await mess_age_.edit(engine.get_string("INPUT_REQ").format("Chat ID"))
        return
    try:
        channel_str = int(chnnl)
    except ValueError:
        channel_str = str(chnnl)
    try:
        u_ = await client.get_chat(channel_str)
    except:
        await mess_age_.edit(engine.get_string("INVALID_CHAT_ID"))
        return
    channel_str = int(u_.id)
    if not await check_if_autopost_in_db(int(message.chat.id), channel_str):
        await mess_age_.edit(engine.get_string("CHAT_NOT_IN_DB"))
        return
    await del_autopost(int(message.chat.id), channel_str)
    await mess_age_.edit(engine.get_string("AUTOPOSTING_2").format(chnnl))


@listen(
    (filters.incoming | filters.outgoing)
    & filters.channel
    & ~filters.edited
    & ~filters.service
)
async def autoposterz(client, message):
    chat_id = message.chat.id
    if not await get_autopost(int(chat_id)):
        return
    channels_set = await get_autopost(int(chat_id))
    if not channels_set:
        return
    for chat in channels_set:
        try:
            await message.copy(int(chat["to_channel"]))
        except Exception as e:
            logging.error(
                f"[AUTOPOST] | {e} | {chat['to_channel']} | {message.chat.id}"
            )
    
