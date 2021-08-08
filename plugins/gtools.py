# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.


from pyrogram import filters

from database.gbandb import gban_info, gban_list, gban_user, ungban_user
from database.gmutedb import gmute, is_gmuted, ungmute
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
from plugins import devs_id
from database.sudodb import sudo_list


@friday_on_cmd(
    ["gmute"],
    cmd_help={
        "help": "Globally Mute The User!",
        "example": "{ch}gmute (reply to user messages OR provide his ID)",
    },
)
async def gmute_him(client, message):
    AFS = await sudo_list()
    engine = message.Engine
    g = await edit_or_reply(message, engine.get_string("PROCESSING"))
    text_ = get_text(message)
    user, reason = get_user(message, text_)
    if not user:
        await g.edit(engine.get_string("REPLY_TO_USER").format("gmute"))
        return
    try:
        userz = await client.get_users(user)
    except:
        await g.edit(engine.get_string("USER_MISSING").format("User Doesn't Exists In This Chat !"))
        return
    if not reason:
        reason = "Just_Gmutted!"
    if userz.id == (client.me).id:
        await g.edit(engine.get_string("TF_DO_IT").format("Gmute"))
        return
    if userz.id in devs_id:
        await g.edit("`Sadly, I Can't Do That!`")
        return
    if userz.id in AFS:
        await g.edit("`Sudo Users Can't Be Gmutted! Remove Him And Try Again!`")
        return
    if await is_gmuted(userz.id):
        await g.edit("`Re-Gmute? Seriously? :/`")
        return
    await gmute(userz.id, reason)
    gmu = f"**#Gmutted** \n**User :** `{userz.id}` \n**Reason :** `{reason}`"
    await g.edit(gmu)
    log = LogIt(message)
    await log.log_msg(client, gmu)


@friday_on_cmd(
    ["ungmute"],
    cmd_help={
        "help": "Globally UnMute The User!",
        "example": "{ch}ungmute (reply to user message OR provide his ID)",
    },
)
async def gmute_him(client, message):
    AFS = await sudo_list()
    engine = message.Engine
    ug = await edit_or_reply(message, engine.get_string("PROCESSING"))
    text_ = get_text(message)
    user_ = get_user(message, text_)[0]
    if not user_:
        await ug.edit(engine.get_string("REPLY_TO_USER").format("UN-gmute"))
        return
    try:
        userz = await client.get_users(user_)
    except BaseException as e:
        await ug.edit(engine.get_string("USER_MISSING").format(e))
        return
    if userz.id == (client.me).id:
        await ug.edit(engine.get_string("TF_DO_IT").format("UN-gmute"))
        return
    if userz.id in AFS:
        await ug.edit("`Sudo Users Can't Be Un-Gmutted! Remove Him And Try Again!`")
        return
    if not await is_gmuted(userz.id):
        await ug.edit("`Un-Gmute A Non Gmutted User? Seriously? :/`")
        return
    await ungmute(userz.id)
    ugmu = f"**#Un-Gmutted** \n**User :** `{userz.id}`"
    await ug.edit(ugmu)
    log = LogIt(message)
    await log.log_msg(client, ugmu)


@friday_on_cmd(
    ["gban"],
    cmd_help={
        "help": "Globally Ban The User!",
        "example": "{ch}gban (reply to user message OR provide his ID)",
    },
)
async def gbun_him(client, message):
    AFS = await sudo_list()
    engine = message.Engine
    gbun = await edit_or_reply(message, engine.get_string("PROCESSING"))
    text_ = get_text(message)
    user, reason = get_user(message, text_)
    failed = 0
    if not user:
        await gbun.edit(engine.get_string("REPLY_TO_USER").format("gban"))
        return
    try:
        userz = await client.get_users(user)
    except BaseException as e:
        await gbun.edit(engine.get_string("USER_MISSING").format(e))
        return
    if not reason:
        reason = "Private Reason!"
    if userz.id == (client.me).id:
        await gbun.edit(engine.get_string("TF_DO_IT").format("GBan"))
        return
    if userz.id in devs_id:
        await g.edit("`Sadly, I Can't Do That!`")
        return
    if userz.id in AFS:
        await gbun.edit("`Sudo Users Can't Be Gbanned! Remove Him And Try Again!`")
        return
    if await gban_info(userz.id):
        await gbun.edit("`Re-Gban? Seriously? :/`")
        return
    await gbun.edit("`Please, Wait Fectching Your Chats!`")
    chat_dict = await iter_chats(client)
    chat_len = len(chat_dict)
    if not chat_dict:
        gbun.edit("`You Have No Chats! So Sad`")
        return
    await gbun.edit(engine.get_string("GBAN_START"))
    for ujwal in chat_dict:
        try:
            await client.kick_chat_member(ujwal, int(userz.id))
        except:
            failed += 1
    await gban_user(userz.id, reason)
    gbanned = f"**#GBanned** \n**User :** [{userz.first_name}](tg://user?id={userz.id}) \n**Reason :** `{reason}` \n**Affected Chats :** `{chat_len-failed}`"
    await gbun.edit(gbanned)
    log = LogIt(message)
    await log.log_msg(client, gbanned)


@friday_on_cmd(
    ["ungban"],
    cmd_help={
        "help": "Globally Unban The User!",
        "example": "{ch}ungban (reply to user messages OR provide his ID)",
    },
)
async def ungbun_him(client, message):
    AFS = await sudo_list()
    engine = message.Engine
    ungbun = await edit_or_reply(message, engine.get_string("PROCESSING"))
    text_ = get_text(message)
    user = get_user(message, text_)[0]
    failed = 0
    if not user:
        await ungbun.edit(engine.get_string("REPLY_TO_USER").format("Un-Gban"))
        return
    try:
        userz = await client.get_users(user)
    except BaseException as e:
        await ungbun.edit(engine.get_string("USER_MISSING").format(e))
        return
    if userz.id == (client.me).id:
        await ungbun.edit(engine.get_string("TF_DO_IT").format("Un-GBan"))
        return
    if not await gban_info(userz.id):
        await ungbun.edit("`Un-Gban A Ungbanned User? Seriously? :/`")
        return
    await ungbun.edit("`Please, Wait Fectching Your Chats!`")
    chat_dict = await iter_chats(client)
    chat_len = len(chat_dict)
    if not chat_dict:
        ungbun.edit("`You Have No Chats! So Sad`")
        return
    await ungbun.edit("`Starting Un-GBans Now!`")
    for ujwal in chat_dict:
        try:
            await client.unban_chat_member(ujwal, int(userz.id))
        except:
            failed += 1
    await ungban_user(userz.id)
    ungbanned = f"**#Un_GBanned** \n**User :** [{userz.first_name}](tg://user?id={userz.id}) \n**Affected Chats :** `{chat_len-failed}`"
    await ungbun.edit(ungbanned)
    log = LogIt(message)
    await log.log_msg(client, ungbanned)


@listen(filters.incoming & ~filters.me & ~filters.user(Config.AFS))
async def watch(client, message):
    AFS = await sudo_list()
    if not message:
        return
    if not message.from_user:
        return
    user = message.from_user.id
    if not user:
        return
    if await is_gmuted(user):
        try:
            await message.delete()
        except:
            return
    if await gban_info(user):
        if message.chat.type == "private":
            return
        try:
            await message.chat.kick_member(int(user))
        except BaseException:
            return
        await client.send_message(
            message.chat.id,
            f"**#GbanWatch** \n**Chat ID :** `{message.chat.id}` \n**User :** `{user}` \n**Reason :** `{await gban_info(user)}`",
        )
    
@friday_on_cmd(
    ["gbanlist"],
    cmd_help={
        "help": "Get List Of Globally Banned Users!",
        "example": "{ch}gbanlist (reply to user messages OR provide his ID)",
    },
)
async def give_glist(client, message):
    engine = message.Engine
    oof = "**#GBanList** \n\n"
    glist = await edit_or_reply(message, engine.get_string("PROCESSING"))
    list_ = await gban_list()
    if len(list_) == 0:
        await glist.edit("`No User is Gbanned Till Now!`")
        return
    for lit in list_:
        oof += f"**User :** `{lit['user']}` \n**Reason :** `{lit['reason']}` \n\n"
    await edit_or_send_as_file(oof, glist, client, "GbanList", "Gban-List")


@friday_on_cmd(
    ["gbroadcast"],
    cmd_help={
        "help": "Send Message To All Chats, You Are In!",
        "example": "{ch}gbroadcast (replying to message)",
    },
)
async def gbroadcast(client, message):
    engine = message.Engine
    msg_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    failed = 0
    if not message.reply_to_message:
        await msg_.edit(engine.get_string("NEEDS_REPLY").format("Message"))
        return
    chat_dict = await iter_chats(client)
    chat_len = len(chat_dict)
    await msg_.edit("`Now Sending To All Chats Possible!`")
    if not chat_dict:
        msg_.edit(engine.get_string("NO_CHATS"))
        return
    for c in chat_dict:
        try:
            msg = await message.reply_to_message.copy(c)
        except:
            failed += 1
    await msg_.edit(
        engine.get_string("BROADCAST_8").format(chat_len-failed, failed)
    )
