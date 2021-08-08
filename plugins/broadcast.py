# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import logging

from database.broadcast_db import (
    add_broadcast_chat,
    get_all_broadcast_chats,
    is_broadcast_chat_in_db,
    rmbroadcast_chat,
)
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@friday_on_cmd(
    ["badd"],
    cmd_help={
        "help": "Add Group/Channel For Broadcast!. Give input as 'all' to add all.",
        "example": "{ch}badd @fridaysupportofficial",
    },
)
async def badd(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    bd = get_text(message)
    if not bd:
        await pablo.edit(engine.get_string("INPUT_REQ").format("Chat ID"))
        return
    if bd.lower() == "all":
        await pablo.edit(engine.get_string("BROADCAST_2"))
        sed = 0
        oks = 0
        zxz = ["channel", "supergroup"]
        nd = ["creator", "administrator"]
        async for dialog in client.iter_dialogs():
            if dialog.chat.type in zxz:
                x = await client.get_chat_member(dialog.chat.id, message.from_user.id)
                if x.status in nd:
                    if not await is_broadcast_chat_in_db(dialog.chat.id):
                        await add_broadcast_chat(dialog.chat.id)
                        oks += 1
                    else:
                        sed += 1
        await pablo.edit(
            engine.get_string("BROADCAST_1").format(oks, oks+sed)
        )
    else:
        chnl_id = await get_final_id(bd, client)
        if not chnl_id:
            await pablo.edit(engine.get_string('CHAT_NOT_IN_DB'))
            return
        chnl_id = int(chnl_id)
        if await is_broadcast_chat_in_db(chnl_id):
            await pablo.edit(engine.get_string("INVALID_CHAT_ID"))
            return
        await add_broadcast_chat(chnl_id)
        await pablo.edit(engine.get_string("BROADCAST_3").format(bd))


@friday_on_cmd(
    ["brm"],
    cmd_help={
        "help": "Remove Group/Channel From Broadcast dB!. Give input as 'all' to Remove all.",
        "example": "{ch}brm @fridaysupportofficial",
    },
)
async def brm(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, "`Processing..`")
    bd = get_text(message)
    if not bd:
        await pablo.edit(engine.get_string("INPUT_REQ").format("Chat ID"))
        return
    if bd.lower() == "all":
        await pablo.edit(engine.get_string(""))
        all = await get_all_broadcast_chats()
        Jill = 0
        for chnnl in all:
            await rmbroadcast_chat(chnnl["chat_id"])
            Jill += 1
        await pablo.edit(engine.get_string("BROADCAST_5").format(Jill))
    else:
        chnl_id = await get_final_id(bd, client)
        if not chnl_id:
            await pablo.edit(engine.get_string("INVALID_CHAT_ID"))
            return
        chnl_id = int(chnl_id)
        if not await is_broadcast_chat_in_db(chnl_id):
            await pablo.edit(engine.get_string("FILTER_1").format("BROADCAST", bd))
            return
        await add_broadcast_chat(chnl_id)
        await pablo.edit(engine.get_string("BROADCAST_4").format(bd))


@friday_on_cmd(
    ["broadcast"],
    cmd_help={
        "help": "Broadcast Message In All Groups/Channels which are added in dB.",
        "example": "{ch}broadcast (replying to broadcast message)",
    },
)
async def broadcast(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(
        message, engine.get_string("BROADCAST_6")
    )
    leat = await get_all_broadcast_chats()
    S = 0
    F = 0
    if len(leat) == 0:
        await pablo.edit(engine.get_string("BROADCAST_7"))
        return
    if not message.reply_to_message:
        await pablo.edit(engine.get_string("REPLY_MSG"))
        return
    for lolol in leat:
        try:
            await client.copy_message(
                chat_id=lolol["chat_id"],
                from_chat_id=message.chat.id,
                message_id=message.reply_to_message.message_id,
            )
            S += 1
        except Exception as e:
            logging.error(f"[Broadcast] {e}")
            F += 1
    await pablo.edit(
        engine.get_string("BROADCAST_8").format(S, F)
    )


async def get_final_id(query, client):
    is_int = True
    try:
        in_t = int(query)
    except ValueError:
        is_int = False
    chnnl = in_t if is_int else str(query)
    try:
        return int((await client.get_chat(chnnl)).id)
    except:
        return None
