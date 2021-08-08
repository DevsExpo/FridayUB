# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters

from database.notesdb import add_note, all_note, del_note, del_notes, note_info
from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd, listen
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@friday_on_cmd(
    ["savenote"],
    cmd_help={
        "help": "Save Notes In The Chat!",
        "example": "{ch}savenote (note name) (reply to Note message)",
    },
)
async def notes(client, message):
    engine = message.Engine
    note_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    note_name = get_text(message)
    if not note_name:
        await note_.edit(engine.get_string("INPUT_REQ").format("Note Name"))
        return
    if not message.reply_to_message:
        await note_.edit(engine.get_string("REPLY_MSG"))
        return
    note_name = note_name.lower()
    msg = message.reply_to_message
    copied_msg = await msg.copy(int(Config.LOG_GRP))
    await add_note(note_name, message.chat.id, copied_msg.message_id)
    await note_.edit(engine.get_string("FILTER_5").format(note_name, "Note"))


@listen(filters.incoming & filters.regex("\#(\S+)"))
async def lmao(client, message):
    engine = message.Engine
    if not await all_note(message.chat.id):
        return
    owo = message.matches[0].group(1)
    if owo is None:
        return
    if await note_info(owo, message.chat.id):
        sed = await note_info(owo, message.chat.id)
        await client.copy_message(
            from_chat_id=int(Config.LOG_GRP),
            chat_id=message.chat.id,
            message_id=sed["msg_id"],
            reply_to_message_id=message.message_id,
        )
    


@friday_on_cmd(
    ["delnote"],
    cmd_help={"help": "Delete Note In The Chat!", "example": "{ch}delnote (Note Name)"},
)
async def notes(client, message):
    engine = message.Engine
    note_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    note_name = get_text(message)
    if not note_name:
        await note_.edit(engine.get_string("INPUT_REQ").format("Note Name"))
        return
    note_name = note_name.lower()
    if not await note_info(note_name, message.chat.id):
        await note_.edit(engine.get_string("FILTER_1").format("NOTE", note_name))
        return
    await del_note(note_name, message.chat.id)
    await note_.edit(engine.get_string("NOT_ADDED").format(note_name))


@friday_on_cmd(
    ["delnotes"],
    cmd_help={"help": "Delete All The Notes In The Chat!", "example": "{ch}delnotes"},
)
async def noteses(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    poppy = await all_note(message.chat.id)
    if poppy is False:
        await pablo.edit(engine.get_string("FILTER_3").format("Notes"))
        return
    await del_notes(message.chat.id)
    await pablo.edit(engine.get_string("REMOVED_ALL").format("Notes"))


@friday_on_cmd(
    ["notes"],
    cmd_help={"help": "List All The Chat Notes!", "example": "{ch}notes"},
)
async def noteses(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    poppy = await all_note(message.chat.id)
    if poppy is False:
        await pablo.edit(engine.get_string("FILTER_3").format("Notes"))
        return
    kk = "".join(f"""\n~ `{Escobar.get("keyword")}`""" for Escobar in poppy)
    X = await client.get_chat(message.chat.id)
    grp_nme = X.title
    mag = engine.get_string("LIST_OF").format("Notes", grp_nme, kk)
    mag += "\n\nGet Notes With `#Notename`"
    await pablo.edit(mag)
