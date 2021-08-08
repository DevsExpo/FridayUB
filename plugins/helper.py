# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.


from main_startup import CMD_LIST, bot, XTRA_CMD_LIST
from main_startup.core.decorators import Config, friday_on_cmd
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text


@friday_on_cmd(
    ["help", "helper"],
    cmd_help={
        "help": "Gets Help Menu",
        "example": "{ch}help",
    },
)
async def help(client, message):
    engine = message.Engine
    f_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    if bot:
        starkbot = bot.me
        bot_username = starkbot.username
        try:
            nice = await client.get_inline_bot_results(bot=bot_username, query="help")
            await client.send_inline_bot_result(
                message.chat.id, nice.query_id, nice.results[0].id, hide_via=True
            )
        except BaseException as e:
            return await f_.edit(engine.get_string("HELP_OPEN_ERROR").format(e))
        await f_.delete()
    else:
        cmd_ = get_text(message)
        if not cmd_:
            help_t = prepare_cmd_list(engine)            
            await f_.edit(help_t)
        else:
            help_s = get_help_str(cmd_)
            if not help_s:
                await f_.edit(engine.get_string("PLUGIN_NOT_FOUND"))
                return
            await f_.edit(help_s)


@friday_on_cmd(
    ["ahelp", "ahelper"],
    cmd_help={
        "help": "Gets Help List & Info",
        "example": "{ch}ahelp (cmd_name)",
    },
)
async def help_(client, message):
    engine = message.Engine
    f_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    cmd_ = get_text(message)
    if not cmd_:
        help_t = prepare_cmd_list(engine)            
        await f_.edit(help_t)
    else:
        help_s = get_help_str(cmd_)
        if not help_s:
            await f_.edit(engine.get_string("PLUGIN_NOT_FOUND"))
            return
        await f_.edit(help_s)

        
def get_help_str(string):
    if string not in CMD_LIST.keys():
        if string not in XTRA_CMD_LIST.keys():
            return None
        return XTRA_CMD_LIST[string]
    return CMD_LIST[string]
    
def prepare_cmd_list(engine):
    main_l = engine.get_string("CMD_LIST_MENU").format(len(CMD_LIST))
    for i in CMD_LIST:
        if i:
            main_l += f"<code>{i}</code>    "
    if Config.LOAD_UNOFFICIAL_PLUGINS:
        main_l += engine.get_string("CMD_LIST_MENU2").format(len(XTRA_CMD_LIST))
        for i in XTRA_CMD_LIST:
            if i:
                main_l += f"<code>{i}</code>    "
    main_l += engine.get_string("KNOW_MORE_ABOUT_PLUGIN").format(Config.COMMAND_HANDLER)
    return main_l 
    
