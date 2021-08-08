# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import os

from pyrogram import filters

from database.bot_settings_db import (
    add_pm_text,
    add_pm_thumb,
    get_pm_spam_limit,
    get_pm_text,
    get_thumb,
    set_pm_spam_limit,
)
from database.pmdb import approve_user, disapprove_user, is_user_approved
from main_startup.core.decorators import friday_on_cmd, listen
from main_startup import Config
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from main_startup.helper_func.logger_s import LogIt
from main_startup.helper_func.plugin_helpers import convert_to_image

PM_WARNS = {}
OLD_MSG = {}

from plugins import devs_id



@friday_on_cmd(
    ["setpmtext"],
    cmd_help={
        "help": "Set Custom On Text!",
        "example": "{ch}setpmtext (reply to Pm Text)",
    },
)
async def set_custom_pm_texts(client, message):
    engine = message.Engine
    if not Config.PM_PSW:
        await message.edit(engine.get_string("SET_PM_TEXT"))
        return
    ptext = get_text(message)
    if not ptext:
        if not message.reply_to_message:
            await message.edit(engine.get_string("TO_SET_CUSTOM_TEXT"))
            return
        if message.reply_to_message.text:
            ptext = message.reply_to_message.text
    if not ptext:
        await message.edit(
            engine.get_string("TO_SET_CUSTOM_TEXT")
        )
        return
    if ptext == "default":
        await add_pm_text()
    else:
        await add_pm_text(ptext)
    await message.edit(engine.get_string("PM_MSG_CHANGED").format(ptext))


@friday_on_cmd(
    ["setpmlimit"],
    cmd_help={
        "help": "Set Pm Limit!",
        "example": "{ch}setpmlimit (number between 3-20)"})
async def set_custom_pm_limit(client, message):
    engine = message.Engine
    if not Config.PM_PSW:
        await message.edit(engine.get_string("SET_PM_LIMIT"))
        return
    ptext = get_text(message)
    if not ptext:
        await message.edit(engine.get_string("INPUT_REQ").format("Pm Limit"))
        return
    if not ptext.isdigit():
        await message.edit(engine.get_string("TO_SET_PM_LIMIT"))
        return
    if int(ptext) < 3:
        await message.edit(engine.get_string("TO_SET_PM_LIMIT"))
        return
    if int(ptext) >= 20:
        await message.edit(engine.get_string("TO_SET_PM_LIMIT"))
        return
    await set_pm_spam_limit(int(ptext))
    await message.edit(engine.get_string("SUCCESS_CHANGED").format(ptext))


@friday_on_cmd(
    ["block"],
    cmd_help={
        "help": "Block Replied User!",
        "example": "{ch}block (reply to user message)",
    },
)
async def blockz(client, message):
    engine = message.Engine
    if message.chat.type == "private":
        user_ = await client.get_users(int(message.chat.id))
        firstname = user_.first_name
        if await is_user_approved(int(message.chat.id)):
            await disapprove_user(int(message.chat.id))
        await message.edit(
            "Blocked [{}](tg://user?id={})".format(firstname, int(message.chat.id))
        )
        await client.block_user(int(message.chat.id))
        await asyncio.sleep(3)
        await message.delete()
    elif message.chat.type == "supergroup":
        if not message.reply_to_message:
            await message.edit(engine.get_string("TO_BLOCK").format("Block"))
            return
        user_ = await client.get_users(message.reply_to_message.from_user.id)
        firstname = user_.first_name
        if await is_user_approved(message.reply_to_message.from_user.id):
            await disapprove_user(message.reply_to_message.from_user.id)
        await message.edit(
            "Blocked [{}](tg://user?id={})".format(
                firstname, message.reply_to_message.from_user.id
            )
        )
        await client.block_user(message.reply_to_message.from_user.id)
        await asyncio.sleep(3)
        await message.delete()


@friday_on_cmd(
    ["unblock"],
    cmd_help={
        "help": "Unblock Replied Uset!",
        "example": "{ch}unblock (reply to user message)",
    },
)
async def unmblock(client, message):
    engine = message.Engine
    if message.chat.type == "private":
        await asyncio.sleep(3)
        await message.delete()
    elif message.chat.type == "supergroup":
        if not message.reply_to_message:
            await message.edit(engine.get_string("TO_BLOCK").format("Un-Block"))
            return
        user_ = await client.get_users(message.reply_to_message.from_user.id)
        firstname = user_.first_name
        await message.edit(
            "Un-Blocked [{}](tg://user?id={})".format(
                firstname, message.reply_to_message.from_user.id
            )
        )
        await client.unblock_user(message.reply_to_message.from_user.id)
        await asyncio.sleep(3)
        await message.delete()


@friday_on_cmd(
    ["a", "accept", "allow"],
    cmd_help={
        "help": "Allow User To Pm you!",
        "example": "{ch}a (reply to user message)",
    },
)
async def allow(client, message):
    engine = message.Engine
    if not Config.PM_PSW:
        await message.edit(engine.get_engine("HACK_APPROVED").format("Approving"))
        return
    if message.chat.type == "private":
        if int(message.chat.id) in OLD_MSG:
            await OLD_MSG[int(message.chat.id)].delete()
        user_ = await client.get_users(int(message.chat.id))
        firstname = user_.first_name
        if not await is_user_approved(int(message.chat.id)):
            await approve_user(int(message.chat.id))
        else:
            await message.edit(engine.get_string("USER_ALREADY_APPROVED").format(message.reply_to_message.from_user.mention))
            await asyncio.sleep(3)
            await message.delete()
            return
        await message.edit(
            "Approved to pm [{}](tg://user?id={})".format(
                firstname, int(message.chat.id)
            )
        )
        await asyncio.sleep(3)
        await message.delete()
    elif message.chat.type == "supergroup":
        if not message.reply_to_message:
            await message.edit(engine.get_string("TO_BLOCK").format("Approve"))
            return
        user_ = await client.get_users(message.reply_to_message.from_user.id)
        firstname = user_.first_name
        if not await is_user_approved(message.reply_to_message.from_user.id):
            await approve_user(message.reply_to_message.from_user.id)
        else:
            await message.edit(engine.get_string("USER_ALREADY_APPROVED").format(message.reply_to_message.from_user.mention))
            await asyncio.sleep(3)
            await message.delete()
            return
        await message.edit(
            "Approved to pm [{}](tg://user?id={})".format(
                firstname, message.reply_to_message.from_user.id
            )
        )
        await asyncio.sleep(3)
        await message.delete()


@friday_on_cmd(
    ["da", "disaccept", "disallow", "disapprove"],
    cmd_help={
        "help": "Disallow User To Pm you!",
        "example": "{ch}da (reply to user message)",
    },
)
async def disallow(client, message):
    engine = message.Engine
    if not Config.PM_PSW:
        await message.edit(engine.get_engine("HACK_APPROVED").format("Dis-Approving"))
        return
    if message.chat.type == "private":
        user_ = await client.get_users(int(message.chat.id))
        firstname = user_.first_name
        if await is_user_approved(int(message.chat.id)):
            await disapprove_user(int(message.chat.id))
        else:
            await message.edit(
                engine.get_string("USER_NOT_APPROVED").format(message.reply_to_message.from_user.mention))
            await asyncio.sleep(3)
            await message.delete()
            return
        await message.edit(
            "DisApproved to pm [{}](tg://user?id={})".format(
                firstname, int(message.chat.id)
            )
        )
        await asyncio.sleep(3)
        await message.delete()
    elif message.chat.type == "supergroup":
        if not message.reply_to_message:
            await message.edit(engine.get_string("TO_BLOCK").format("Disapprove"))
            return
        user_ = await client.get_users(message.reply_to_message.from_user.id)
        firstname = user_.first_name
        if await is_user_approved(message.reply_to_message.from_user.id):
            await disapprove_user(message.reply_to_message.from_user.id)
        else:
            await message.edit(
                engine.get_string("USER_NOT_APPROVED").format(message.reply_to_message.from_user.mention))
            await asyncio.sleep(3)
            await message.delete()
            return
        await message.edit(
            "DisApproved to pm [{}](tg://user?id={})".format(
                firstname, message.reply_to_message.from_user.id
            )
        )
        await asyncio.sleep(3)
        await message.delete()


@friday_on_cmd(
    ["setpmpic", "spp"],
    cmd_help={
        "help": "Set Replied Image As Your Pm Permit Image.",
        "example": "{ch}setpmpic (reply to image)",
    },
)
async def set_my_pic(client, message):
    engine = message.Engine
    ms_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    if not Config.PM_PSW:
        await message.edit("`Pm Permit Is Disabled. Whats The Use Of Adding A Pm Pic?`")
        return
    if not await is_media(message.reply_to_message):
        await ms_.edit(engine.get_string("NEEDS_REPLY").format("Media"))
        return
    if message.reply_to_message.sticker:
        file_ = await convert_to_image(message, client)
        if not os.path.exists(file_):
            return await ms_.edit(engine.get_string("NEEDS_C_INPUT"))
        copied_msg = await client.send_photo(Config.LOG_GRP, file_)
        if os.path.exists(file_):
            os.remove(file_)
    else:
        copied_msg = await message.reply_to_message.copy(int(Config.LOG_GRP), caption="")
    await add_pm_thumb(copied_msg.message_id)
    await ms_.edit(engine.get_string("SET_DONE_IMAGE"))

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

@listen(filters.incoming & filters.private & ~filters.edited & ~filters.me & ~filters.service)
async def pmPermit(client, message):
    if not Config.PM_PSW:
        return
    if not message.from_user:   
        return
    if await is_user_approved(int(message.chat.id)):
        return
    if message.from_user.id in devs_id:
        await approve_user(int(message.chat.id))
        return
    user_ = message.from_user
    if user_.is_bot:
        return
    if user_.is_self:
        return
    if user_.is_verified:       
        return
    if user_.is_scam:
        await message.reply_text("`Scammer Aren't Welcome To My Masters PM!`")
        await client.block_user(user_.id)
        return
    if user_.is_support:
        return
    text = await get_pm_text()
    log = LogIt(message)
    capt = await get_thumb()
    pm_s_ = await get_pm_spam_limit()
    if int(message.chat.id) not in PM_WARNS:
        PM_WARNS[int(message.chat.id)] = 0
    else:
        PM_WARNS[int(message.chat.id)] += 1
    if PM_WARNS[int(message.chat.id)] >= int(pm_s_):
        await message.reply_text(
            f"`Thats It! I Gave You {int(pm_s_)} Warning. Now Fuck Off. Blocked And Reported!`"
        )
        await client.block_user(user_.id)
        if int(message.chat.id) in OLD_MSG:
            OLD_MSG.pop(int(message.chat.id))
        if int(message.chat.id) in PM_WARNS:
            PM_WARNS.pop(int(message.chat.id))
        blockeda = f"**#Blocked_PMPERMIT** \n**User :** `{user_.id}` \n**Reason :** `Spam Limit Reached.`"
        await log.log_msg(client, blockeda)
        return
    warnings_got = f"{int(PM_WARNS[int(message.chat.id)]) + 1}/{int(pm_s_)}"
    user_firstname = message.from_user.first_name
    user_mention = message.from_user.mention
    me_f = client.me.first_name
    de_pic = "logo.jpg"
    if capt:
        holy = await client.copy_message(
                from_chat_id=int(Config.LOG_GRP),
                message_id=int(capt),
                chat_id=int(message.chat.id),
                caption=text.format(user_firstname=user_firstname, warns=warnings_got, boss_firstname=me_f, mention=user_mention),
                reply_to_message_id=message.message_id
        )
    else:
        holy = await message.reply_photo(
        de_pic,
        caption=text.format(
            user_firstname=user_firstname, warns=warnings_got, boss_firstname=me_f, mention=user_mention),
    )      
    if int(message.chat.id) in OLD_MSG:
        try:
            await OLD_MSG[int(message.chat.id)].delete()
        except:
            pass
    OLD_MSG[int(message.chat.id)] = holy
