# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.


from pyrogram import filters

from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd, listen
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
    get_user,
    iter_chats,
)
from main_startup.helper_func.logger_s import LogIt
from database.sudodb import is_user_sudo, sudo_list, add_sudo, rm_sudo
from plugins import devs_id


@friday_on_cmd(['addsudo'],
              disable_sudo=True,
              cmd_help={
                "help": "Add User To Sudo List.",
                "example": "{ch}addsudo (reply_to_user)",
    })
async def add_s_sudo(client, message):
    engine = message.Engine
    msg_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    text_ = get_text(message)
    user = get_user(message, text_)[0]
    if not user:
        await msg_.edit(engine.get_string("REPLY_TO_USER").format("Sudo"))
        return
    try:
        user = await client.get_users(user)
    except BaseException as e:
        await msg_.edit(engine.get_string("USER_MISSING").format(e))
        return
    if user.id == client.me.id:
        await msg_.delete()
        return
    if await is_user_sudo(user.id):
      return await msg_.edit(engine.get_string("USER_ALREADY_IN_SUDODB").format(user.mention))
    await add_sudo(int(user.id))
    await msg_.edit(engine.get_string("ADDED_TO_SUDO").format(user.mention))
    
@friday_on_cmd(['rmsudo'],
              disable_sudo=True,
              cmd_help={
                "help": "Remove User From Sudo List.",
                "example": "{ch}rmsudo (reply_to_user)",
    })
async def rm_s_sudo(client, message):
    engine = message.Engine
    msg_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    text_ = get_text(message)
    user = get_user(message, text_)[0]
    if not user:
        await msg_.edit(engine.get_string("REPLY_TO_USER").format("Un-Sudo"))
        return
    try:
        user = await client.get_users(user)
    except BaseException as e:
        await msg_.edit(engine.get_string("USER_MISSING").format(e))
        return
    if not await is_user_sudo(user.id):
      return await msg_.edit(engine.get_string("USER_ALREADY_NOT_IN_SUDODB").format(user.mention))
    await rm_sudo(int(user.id))
    await msg_.edit(engine.get_string("RM_FROM_SUDO").format(user.mention))
