# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import time

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, progress


@friday_on_cmd(
    ["rename", "rupload"],
    cmd_help={
        "help": "Rename File!",
        "example": "{ch}rename (reply to file) (new name)",
    },
)
async def rename(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    fname = get_text(message)
    if not fname:
        await pablo.edit(engine.get_string("INPUT_REQ").format("File Name"))
        return
    if not message.reply_to_message:
        await pablo.edit(engine.get_string("NEEDS_REPLY").format("Media"))
        return
    await pablo.edit(engine.get_string("R_P"))
    file_name = None
    try:
        file_name = message.reply_to_message.document.file_name
    except:
        pass
    if file_name:
        Kk = fname.split(".")
        try:
            Kk[1]
        except:
            fuck = file_name.rpartition(".")[-1]
            fname = fname + "." + fuck
    EsCoBaR = await message.reply_to_message.download(fname)
    caption = message.reply_to_message.caption or ""
    c_time = time.time()
    await client.send_document(
        message.chat.id,
        EsCoBaR,
        caption=caption,
        progress=progress,
        progress_args=(pablo, c_time, f"`Uploading {fname}`", EsCoBaR),
    )
    await pablo.delete()
