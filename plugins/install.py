# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import os

from main_startup.core.decorators import friday_on_cmd
from main_startup.core.startup_helpers import load_plugin
from main_startup.helper_func.basic_helpers import edit_or_reply


@friday_on_cmd(
    ["install"],
    cmd_help={
        "help": "Install Custom Plugins In Userbot",
        "example": "{ch}install (replying to plugin (.py))",
    },
)
async def installer(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    if not message.reply_to_message:
        await pablo.edit(engine.get_string("NEEDS_REPLY").format("A Plugin"))
        return
    if not message.reply_to_message.document:
        await pablo.edit(engine.get_string("IS_NOT_DOC"))
        return
    file_name = message.reply_to_message.document.file_name
    ext = file_name.split(".")[1]
    if os.path.exists(os.path.join("./plugins/", file_name)):
        await pablo.edit(engine.get_string("ALREADY_INSTALLED"))
        return
    if ext.lower() != "py":
        await pablo.edit(engine.get_string("ONLY_PY_FILES"))
        return
    Escobar = await message.reply_to_message.download(file_name="./plugins/")
    base_name = os.path.basename(Escobar)
    file_n = base_name.split(".")[0]
    try:
        load_plugin(file_n)
    except Exception as e:
        await pablo.edit(engine.get_string("ERROR_INSTALLING").format(e))
        os.remove(Escobar)
        return
    await pablo.edit(engine.get_string("PLUGIN_INSTALLED").format(file_name))
