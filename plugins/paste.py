# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import os
import aiohttp
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text



@friday_on_cmd(
    ["paste"],
    cmd_help={
        "help": "Pastes The File Text In Nekobin!",
        "example": "{ch}paste (reply to file)",
    },
)
async def paste(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    tex_t = get_text(message)
    message_s = tex_t
    if not tex_t:
        if not message.reply_to_message:
            await pablo.edit(engine.get_string("NEEDS_REPLY").format("File / Text"))
            return
        if not message.reply_to_message.text:
            file = await message.reply_to_message.download()
            m_list = open(file, "r").read()
            message_s = m_list
            os.remove(file)
        else:
            message_s = message.reply_to_message.text
    url = "https://hastebin.com/documents"
    if not message_s:
        await pablo.edit(engine.get_string("NEEDS_REPLY").format("File / Text"))
        return
    async with aiohttp.ClientSession() as session:
        req = await session.post(url, data=message_s.encode('utf-8'), timeout=3)
        resp = await req.json()
    key = resp.get("key")
    url = f"https://hastebin.com/{key}"
    raw = f"https://hastebin.com/raw/{key}"
    reply_text = engine.get_string("PASTED").format(url, raw)
    await pablo.edit(reply_text)
