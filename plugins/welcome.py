# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters

from database.welcomedb import add_welcome, del_welcome, welcome_info
from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd, listen
from main_startup.helper_func.basic_helpers import edit_or_reply


@friday_on_cmd(
    ["savewelcome"],
    cmd_help={
        "help": "Save Welcome Message!",
        "example": "{ch}savewelcome (reply to welcome message)",
    },
)
async def save_welcome(client, message):
    engine = message.Engine
    note_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    if not message.reply_to_message:
        await note_.edit(engine.get_string("REPLY_TO_WELCOME"))
        return
    msg = message.reply_to_message
    cool = await msg.copy(int(Config.LOG_GRP))
    await add_welcome(int(message.chat.id), cool.message_id)
    await note_.edit(engine.get_string("WELCOME_SAVED"))


@listen(filters.new_chat_members & filters.group)
async def welcomenibba(client, message):
    engine = message.Engine
    if not message:    
        return
    if not await welcome_info(int(message.chat.id)):
        return
    if not message.chat:
        return
    is_m = False
    sed = await welcome_info(int(message.chat.id))
    m_s = await client.get_messages(int(Config.LOG_GRP), sed["msg_id"])
    if await is_media(m_s):
        text_ = m_s.caption or ""
        is_m = True
    else:
        text_ = m_s.text or ""
    if text_ != "":
        mention = message.new_chat_members[0].mention
        user_id = message.new_chat_members[0].id
        user_name = message.new_chat_members[0].username or "No Username"
        first_name = message.new_chat_members[0].first_name
        last_name = message.new_chat_members[0].last_name or "No Last Name"
        text_ = text_.format(mention=mention, user_id=user_id, user_name=user_name, first_name=first_name, last_name=last_name)
    if not is_m:
        await client.send_message(
            message.chat.id,
            text_,
            reply_to_message_id=message.message_id)
    else:
        await m_s.copy(
            chat_id=int(message.chat.id),
            caption=text_,
            reply_to_message_id=message.message_id,
        )
    
    
    
async def is_media(message):
    return bool(
        (
            message.photo
            or message.video
            or message.document
            or message.audio
            or message.sticker
            or message.animation
            or message.voice
            or message.video_note
        )
    )


@friday_on_cmd(
    ["delwelcome"],
    cmd_help={"help": "Delete welcome Message!", "example": "{ch}delwelcome"},
)
async def del_welcomez(client, message):
    engine = message.Engine
    note_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    if not await welcome_info(int(message.chat.id)):
        await note_.edit(engine.get_string("FILTER_3").format("Welcome Message"))
        return
    await del_welcome(int(message.chat.id))
    await note_.edit(engine.get_string("FILTER_2").format("Welcome", "Message"))


@friday_on_cmd(
    ["welcome"],
    cmd_help={"help": "Current Welcome Message!", "example": "{ch}welcome"},
)
async def show_welcome(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    sed = await welcome_info(int(message.chat.id))
    if sed is False:
        await pablo.edit(engine.get_string("FILTER_3").format("Welcome Message"))
        return
    mag = f""" Welcome Message In Correct Chat Is :"""
    await client.copy_message(
        from_chat_id=int(Config.LOG_GRP),
        chat_id=int(message.chat.id),
        message_id=sed["msg_id"],
        reply_to_message_id=message.message_id,
    )
    await pablo.edit(mag)
