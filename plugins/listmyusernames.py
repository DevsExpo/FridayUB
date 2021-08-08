# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import pyrogram

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, edit_or_send_as_file


@friday_on_cmd(
    ["listmyusernames"],
    cmd_help={
        "help": "Get All Admin Channel / Chat List",
        "example": "{ch}listmyusernames",
    },
)
async def pabloescobar(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    channels = await client.send(
        pyrogram.raw.functions.channels.GetAdminedPublicChannels()
    )
    C = channels.chats
    output_stre = "".join(f"{x.title}\n@{x.username}\n\n" for x in C)
    output_str = engine.get_string("IAM_ADMIN").format("output_stre")
    await edit_or_send_as_file(
        output_str, pablo, client, "Your Admin Chats", "admin_chat"
    )
