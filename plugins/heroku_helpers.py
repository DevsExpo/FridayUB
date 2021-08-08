# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import os
import time
from asyncio import sleep
from functools import wraps

import heroku3
from pyrogram.types import ChatPermissions

from main_startup.config_var import Config
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
    get_user,
    is_admin_or_owner,
)

heroku_client = None
if Config.HEROKU_API_KEY:
    heroku_client = heroku3.from_key(Config.HEROKU_API_KEY)


def _check_heroku(func):
    @wraps(func)
    async def heroku_cli(client, message):
        engine = message.Engine
        heroku_app = None
        if not heroku_client or not Config.HEROKU_APP_NAME:
            await edit_or_reply(
                message, engine.get_string("MISSING_API_KEY").format("HEROKU_API_KEY")
            )
        if Config.HEROKU_APP_NAME and heroku_client:
            try:
                heroku_app = heroku_client.app(Config.HEROKU_APP_NAME)
            except:
                await edit_or_reply(
                    message, engine.get_string("HEROKU_DONT_MATCH")
                )
            if heroku_app:
                await func(client, message, heroku_app)

    return heroku_cli


@friday_on_cmd(
    ["reboot"],
    cmd_help={"help": "Restart Your Userbot On HEROKU!", "example": "{ch}restart"},
)
@_check_heroku
async def gib_restart(client, message, hap):
    engine = message.Engine
    msg_ = await edit_or_reply(message, engine.get_string("RESTART"))
    hap.restart()


@friday_on_cmd(
    ["logs"], cmd_help={"help": "Get Logs From HEROKU!", "example": "{ch}logs"}
)
@_check_heroku
async def gib_logs(client, message, happ):
    engine = message.Engine
    msg_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    logs = happ.get_log()
    capt = f"Heroku Logs Of {Config.HEROKU_APP_NAME}"
    await edit_or_send_as_file(logs, msg_, client, capt, "logs")


@friday_on_cmd(
    ["setvar"],
    cmd_help={
        "help": "Set Var From telegram Itself, Please Seperate Var And Value With '|'",
        "example": "{ch}setvar LOAD_UNOFFICIAL_PLUGINS False",
    },
)
@_check_heroku
async def set_varr(client, message, app_):
    engine = message.Engine
    msg_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    heroku_var = app_.config()
    _var = get_text(message)
    syntax = f"{Config.COMMAND_HANDLER}setvar ConfigVarName ConfigVarValue"
    if not _var:
        await msg_.edit(engine.get_string("USAGE").format(syntax))
        return
    if " " not in _var:
        await msg_.edit(engine.get_string("USAGE").format(syntax))
        return
    var_ = _var.split(" ", 1)
    if len(var_) > 2:
        await msg_.edit(engine.get_string("USAGE").format(syntax))
        return
    _varname, _varvalue = var_
    s = engine.get_string("VAR_ADDED").format(_varname, _varvalue)
    await msg_.edit(s)
    heroku_var[_varname] = _varvalue


@friday_on_cmd(
    ["delvar"],
    cmd_help={
        "help": "Delete Var From telegram Itself",
        "example": "{ch}delvar LOAD_UNOFFICIAL_PLUGINS",
    },
)
@_check_heroku
async def del_varr(client, message, app_):
    engine = message.Engine
    msg_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    heroku_var = app_.config()
    _var = get_text(message)
    if not _var:
        await msg_.edit(engine.get_string("INPUT_REQ").format("Var Name"))
        return
    if _var not in heroku_var:
        await msg_.edit(engine.get_string("DE"))
        return
    await msg_.edit(engine.get_string("DLTED_VAR").format(_var))
    del heroku_var[_var]
