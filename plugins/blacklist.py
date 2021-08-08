# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import logging

from pyrogram import filters

from database.blacklistdb import (
    add_to_blacklist,
    blacklists_del,
    del_blacklist,
    get_chat_blacklist,
    is_blacklist_in_db,
)
from main_startup.core.decorators import friday_on_cmd, listen
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
)
from main_startup.helper_func.logger_s import LogIt


@friday_on_cmd(
    [
        "saveblacklist",
        "saveblockist",
        "addblacklist",
        "addblocklist",
        "blacklist",
        "textblacklist",
    ],
    cmd_help={
        "help": "Adds Text Blacklist / Blocklist!",
        "example": "{ch}blacklist porn",
    },
)
async def addblacklist(client, message):
    engine = message.Engine
    messag_e_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    blacklist = get_text(message)
    if not blacklist:
        await messag_e_.edit(engine.get_string("INPUT_REQ").format("KeyWord"))
        return
    if await is_blacklist_in_db(int(message.chat.id), blacklist):
        await messag_e_.edit(engine.get_string("BLACKLIST_1"))
        return
    blacklist = blacklist.lower()
    await add_to_blacklist(blacklist, int(message.chat.id))
    await messag_e_.edit(engine.get_string('BLACKLIST_2').format(blacklist))


@friday_on_cmd(
    ["listblacklist", "listblocklist"],
    cmd_help={"help": "Check Blacklist List!", "example": "{ch}listblocklist"},
)
async def listblacklist(client, message):
    engine = message.Engine
    messag_e_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    if not await get_chat_blacklist(int(message.chat.id)):
        await messag_e_.edit(engine.get_string("BLACKLIST_3"))
        return
    OUT_STR = engine.get_string("BLACKLIST_4")
    for trigger_s_ in await get_chat_blacklist(int(message.chat.id)):
        OUT_STR += f"👉 `{trigger_s_['trigger']}` \n"
    await edit_or_send_as_file(OUT_STR, messag_e_, client, "Blacklist", "blacklist")


@friday_on_cmd(
    ["delblacklist", "rmblacklist", "delblockist", "rmblocklist"],
    cmd_help={
        "help": "Remove Text From Blacklist / Blocklist!",
        "example": "{ch}blacklist porn",
    },
)
async def delblacklist(client, message):
    engine = message.Engine
    messag_e_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    blacklist = get_text(message)
    if not blacklist:
        await messag_e_.edit(engine.get_string("INPUT_REQ").format("KeyWord"))
        return
    if not await is_blacklist_in_db(int(message.chat.id), blacklist):
        await messag_e_.edit(engine.get_string("BLACKLIST_5"))
        return
    blacklist = blacklist.lower()
    await del_blacklist(blacklist, int(message.chat.id))
    await messag_e_.edit(engine.get_string("BLACKLIST_6").format(blacklist))


@listen(filters.incoming & ~filters.edited & filters.group)
async def activeblack(client, message):
    engine = message.Engine
    if not await get_chat_blacklist(int(message.chat.id)):
        return
    owo = message.text
    if owo is message.text:
        return
    owoo = owo.lower()
    tges = owoo.split(" ")
    for owo in tges:
        if await is_blacklist_in_db(int(message.chat.id), owo):
            try:
                await message.delete()
            except Exception as e:
                logging.error(f"[Blacklist] - {e}")
                log = LogIt(message)
                await log.log_msg(
                    client,
                    engine.get_strings("BLACKLIST_7").format(message.chat.title, e)
                )
    


@friday_on_cmd(
    ["delblacklists", "rmblacklists", "delblockists", "rmblocklists"],
    cmd_help={
        "help": "Remove Everything From Blocklist!",
        "example": "{ch}delblacklists",
    },
)
async def delblacklists(client, message):
    engine = message.Engine
    messag_e_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    if not await get_chat_blacklist(int(message.chat.id)):
        await messag_e_.edit(engine.get_string("BLACKLIST_3"))
        return
    await blacklists_del(int(message.chat.id))
    await messag_e_.edit(engine.get_string("BLACKLIST_8"))