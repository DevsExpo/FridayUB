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

from pyrogram.types import ChatPermissions
import pyrogram
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
    get_user,
    is_admin_or_owner,
)
from main_startup.helper_func.logger_s import LogIt
from main_startup.helper_func.plugin_helpers import (
    convert_to_image,
    convert_vid_to_vidnote,
    generate_meme,
)


@friday_on_cmd(
    ["silentpin"],
    only_if_admin=True,
    cmd_help={
        "help": "Pin Message Without Sending Notification To Members!",
        "example": "{ch}silentpin (reply to message)",
    },
)
async def spin(client, message):
    engine = message.Engine
    if not message.reply_to_message:
        await edit_or_reply(message, engine.get_string("REPLY_TO_PIN"))
    try:
        await client.pin_chat_message(
            message.chat.id,
            message.reply_to_message.message_id,
            disable_notification=True,
        )
    except BaseException as e:
        await edit_or_reply(
            message, engine.get_string("UNABLE_TO_PIN").format(e)
        )
        return
    await edit_or_reply(message, engine.get_string("PINNED"))


@friday_on_cmd(
    ["pinloud", "pin"],
    only_if_admin=True,
    cmd_help={
        "help": "Pin Message With Sending Notification To Members!",
        "example": "{ch}pin (reply to messages)",
    },
)
async def lpin(client, message):
    engine = message.Engine
    if not message.reply_to_message:
        await edit_or_reply(message, engine.get_string("REPLY_TO_PIN"))
    try:
        await client.pin_chat_message(
            message.chat.id, message.reply_to_message.message_id
        )
    except BaseException as e:
        await edit_or_reply(
            message, engine.get_string("UNABLE_TO_PIN").format(e)
        )
        return
    await edit_or_reply(message, engine.get_string("PINNED"))


@friday_on_cmd(
    ["unpin", "rmpins"],
    only_if_admin=True,
    cmd_help={"help": "Unpin All Pinned Messages!", "example": "{ch}rmpins"},
)
async def dpins(client, message):
    engine = message.Engine
    await client.unpin_all_chat_messages(message.chat.id)
    await edit_or_reply(message, engine.get_string("UNPINNED"))


@friday_on_cmd(
    ["adminlist", "admins"],
    cmd_help={"help": "Get Adminlist Of Chat!", "example": "{ch}adminlist"},
)
async def midhunadmin(client, message):
    engine = message.Engine
    mentions = ""
    starky = get_text(message) or message.chat.id
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    try:
        X = await client.get_chat_members(starky, filter="administrators")
        ujwal = await client.get_chat(starky)
    except BaseException as e:
        await pablo.edit(engine.get_string("CANT_FETCH_ADMIN").format("Admins", e))
        return
    for midhun in X:
        if not midhun.user.is_deleted:
            link = f'✱ <a href="tg://user?id={midhun.user.id}">{midhun.user.first_name}</a>'
            userid = f"<code>{midhun.user.id}</code>"
            mentions += f"\n{link} {userid}"
    holy = ujwal.username or ujwal.id
    messag = f"""
<b>Admins in {ujwal.title} | {holy}</b>

{mentions}
"""
    await edit_or_send_as_file(
        messag,
        pablo,
        client,
        f"`AdminList Of {holy}!`",
        "admin-lookup-result",
        "html",
    )


@friday_on_cmd(
    ["botlist", "bot"],
    group_only=True,
    cmd_help={"help": "Get List Of Bots In Chat!", "example": "{ch}botlist"},
)
async def bothub(client, message):
    engine = message.Engine
    buts = "**Bot List** \n\n"
    starky = get_text(message) or message.chat.id
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    try:
        bots = await client.get_chat_members(starky, filter="bots")
    except BaseException as e:
        await pablo.edit(engine.get_string("CANT_FETCH_ADMIN").format("Bots", e))
        return
    for nos, ujwal in enumerate(bots, start=1):
        buts += f"{nos}〉 [{ujwal.user.first_name}](tg://user?id={ujwal.user.id}) \n"
    await pablo.edit(buts)


@friday_on_cmd(
    ["zombies", "delusers"],
    cmd_help={
        "help": "Remove Deleted Accounts In The Group/Channel!",
        "example": "{ch}zombies",
    },
)
async def ujwalzombie(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    if len(message.text.split()) == 1:
        dm = 0
        da = 0
        dc = 0
        async for member in client.iter_chat_members(message.chat.id):
            if member.user.is_deleted:
                await sleep(1)
                if member.status == "member":
                    dm += 1
                elif member.status == "administrator":
                    da += 1
                elif member.status == "creator":
                    dc += 1
        text = "**Zombies Report!** \n\n"
        if dm > 0:
            text += engine.get_string("TOTAL_ZOMBIES_USERS").format(dm)
        if da > 0:
            text += engine.get_string("TOTAL_ZOMBIES_ADMINS").format(da)
        if dc > 0:
            text += engine.get_string("GRP_OWNER_IS_ZOMBIE")
        d = dm + da + dc
        if d > 0:
            text += (engine.get_string("WIPE_THEM"))
            await pablo.edit(text)
        else:
            await pablo.edit(engine.get_string("NO_ZOMBIES"))
        return
    sgname = message.text.split(None, 1)[1]
    if sgname.lower().strip() == "clean":
        me = client.me
        lol = await is_admin_or_owner(message, me.id)
        if not lol:
            await pablo.edit(engine.get_string("NOT_ADMIN"))
            return
        s = 0
        f = 0
        async for member in client.iter_chat_members(message.chat.id):
            if member.user.is_deleted:
                try:
                    await client.kick_chat_member(message.chat.id, member.user.id)
                    s += 1
                except:
                    f += 1
        text = ""
        if s > 0:
            text += engine.get_string("REMOVED_ZOMBIES").format(s)
        if f > 0:
            text += (engine.get_string("FAILED_ZOMBIES").format(f))
        await pablo.edit(text)


@friday_on_cmd(
    ["ban", "bun"],
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "Ban Replied User or provide his ID!",
        "example": "{ch}ban (reply to user message OR provide his ID)",
    },
)
async def ban_world(client, message):
    engine = message.Engine
    bun = await edit_or_reply(message, engine.get_string("PROCESSING"))
    me_m = client.me
    me_ = await message.chat.get_member(int(me_m.id))
    if not me_.can_restrict_members:
        await bun.edit(engine.get_string("NOT_ADMIN"))
        return
    text_ = get_text(message)
    userk, reason = get_user(message, text_)
    if not userk:
        await bun.edit(engine.get_string("TO_DO").format("Ban"))
        return
    try:
        user_ = await client.get_users(userk)
    except BaseException as e:
        await bun.edit(engine.get_string("USER_MISSING").format(e))
        return
    userz = user_.id
    if not reason:
        reason = "Not Specified!"
    if userz == me_m.id:
        await bun.edit(engine.get_string("TF_DO_IT").format("Ban"))
        return
    try:
        user_ = await client.get_users(userz)
    except BaseException as e:
        await bun.edit(engine.get_string("USER_MISSING").format(e))
        return
    try:
        await client.kick_chat_member(message.chat.id, int(user_.id))
    except BaseException as e:
        await bun.edit(engine.get_string("FAILED_ADMIN_ACTION").format("Ban", e))
        return
    b = f"**#Banned** \n**User :** [{user_.first_name}](tg://user?id={user_.id}) \n**Chat :** `{message.chat.title}` \n**Reason :** `{reason}`"
    await bun.edit(b)
    log = LogIt(message)
    await log.log_msg(client, b)


@friday_on_cmd(
    ["unban", "unbun"],
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "UnBan Replied User or provide his ID!",
        "example": "{ch}unban (reply to user message OR Provide his id)",
    },
)
async def unban_world(client, message):
    engine = message.Engine
    unbun = await edit_or_reply(message, engine.get_string("PROCESSING"))
    me_m = client.me
    me_ = await message.chat.get_member(int(me_m.id))
    if not me_.can_restrict_members:
        await unbun.edit(engine.get_string("NOT_ADMIN"))
        return
    text_ = get_text(message)
    userm, reason = get_user(message, text_)
    if not userm:
        await unbun.edit(
            engine.get_string("TO_DO").format("Un-Ban")
        )
        return
    try:
        user_ = await client.get_users(userm)
    except BaseException as e:
        await unbun.edit(engine.get_string("USER_MISSING").format(e))
        return
    userz = user_.id
    if not reason:
        reason = "Not Specified!"
    if userz == me_m.id:
        await unbun.edit(engine.get_string("TF_DO_IT").format("Un-Ban"))
        return
    try:
        await client.unban_chat_member(message.chat.id, int(user_.id))
    except BaseException as e:
        await unbun.edit(engine.get_string("FAILED_ADMIN_ACTION").format("Un-Ban", e))
    ub = f"**#UnBanned** \n**User :** [{user_.first_name}](tg://user?id={user_.id}) \n**Chat :** `{message.chat.title}` \n**Reason :** `{reason}`"
    await unbun.edit(ub)
    log = LogIt(message)
    await log.log_msg(client, ub)


@friday_on_cmd(
    ["promote", "prumote"],
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "Promote Replied user or provide his ID!",
        "example": "{ch}promote (reply to user message OR provide his ID)",
    },
)
async def ujwal_mote(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    me_m = client.me
    me_ = await message.chat.get_member(int(me_m.id))
    if not me_.can_promote_members:
        await pablo.edit(engine.get_string("NOT_ADMIN"))
        return
    asplit = get_text(message)
    userl, Res = get_user(message, asplit)
    if not userl:
        await pablo.edit(
            engine.get_string("TO_DO").format("Promote")
        )
        return
    try:
        user = await client.get_users(userl)
    except BaseException as e:
        await pablo.edit(engine.get_string("USER_MISSING").format(e))
        return
    userz = user.id
    if not Res:
        Res = "Admeme"
    if userz == me_m.id:
        await pablo.edit(engine.get_string("TF_DO_IT").format("Promote"))
        return
    try:
        await client.promote_chat_member(
            message.chat.id,
            user.id,
            can_change_info=me_.can_change_info,
            can_delete_messages=me_.can_delete_messages,
            can_restrict_members=me_.can_restrict_members,
            can_invite_users=me_.can_invite_users,
            can_pin_messages=me_.can_pin_messages,
            can_promote_members=me_.can_promote_members,
        )
    except BaseException as e:
        await pablo.edit(engine.get_string("FAILED_ADMIN_ACTION").format("Promote", e))
        return
    p = f"**#Promote** \n**User :** [{user.first_name}](tg://user?id={user.id}) \n**Chat :** `{message.chat.title}` \n**Title :** `{Res}`"
    await pablo.edit(p)
    log = LogIt(message)
    await log.log_msg(client, p)
    try:
        if Res:
            await client.set_administrator_title(message.chat.id, user.id, Res)
    except:
        pass


@friday_on_cmd(
    ["demote", "demute"],
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "Demote Replied user or provide his ID!",
        "example": "{ch}demote (reply to user message OR provide his ID)",
    },
)
async def ujwal_demote(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    me_m = client.me
    await message.chat.get_member(int(me_m.id))
    asplit = get_text(message)
    usero = get_user(message, asplit)[0]
    if not usero:
        await pablo.edit(
            engine.get_string("TO_DO").format("Demote")
        )
        return
    try:
        user = await client.get_users(usero)
    except BaseException as e:
        await pablo.edit(engine.get_string("USER_MISSING").format(e))
        return
    userz = user.id
    if userz == me_m.id:
        await pablo.edit(engine.get_string("TF_DO_IT").format("Demote"))
        return
    try:
        await client.promote_chat_member(
            message.chat.id,
            user.id,
            is_anonymous=False,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        )
    except BaseException as e:
        await pablo.edit(engine.get_string("FAILED_ADMIN_ACTION").format("Demote", e))
        return
    d = f"**#Demote** \n**User :** [{user.first_name}](tg://user?id={user.id}) \n**Chat :** `{message.chat.title}`"
    await pablo.edit(d)
    log = LogIt(message)
    await log.log_msg(client, d)


@friday_on_cmd(
    ["mute"],
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "Mute Replied user or provide his ID!",
        "example": "{ch}mute (reply to user message OR provide his ID)",
    },
)
async def ujwal_mute(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    me_m = client.me
    me_ = await message.chat.get_member(int(me_m.id))
    if not me_.can_restrict_members:
        await pablo.edit(engine.get_string("NOT_ADMIN"))
        return
    asplit = get_text(message)
    userf = get_user(message, asplit)[0]
    if not userf:
        await pablo.edit(
            engine.get_string("TO_DO").format("Mute")
        )
        return
    try:
        user = await client.get_users(userf)
    except BaseException as e:
        await pablo.edit(engine.get_string("USER_MISSING").format(e))
        return
    userz = user.id
    if userz == me_m.id:
        await pablo.edit(engine.get_string("TF_DO_IT").format("Mute"))
        return
    try:
        await client.restrict_chat_member(
            message.chat.id, user.id, ChatPermissions(can_send_messages=False)
        )
    except BaseException as e:
        await pablo.edit(engine.get_string("FAILED_ADMIN_ACTION").format("Mute", e))
        return
    m = f"**#Muted** \n**User :** [{user.first_name}](tg://user?id={user.id}) \n**Chat :** `{message.chat.title}`"
    await pablo.edit(m)
    log = LogIt(message)
    await log.log_msg(client, m)


@friday_on_cmd(
    ["unmute"],
    only_if_admin=True,
    group_only=True,
    cmd_help={
        "help": "Unmute Replied user or provide his ID!",
        "example": "{ch}Unmute (reply to user message OR provide his ID)",
    },
)
async def ujwal_unmute(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    me_m = client.me
    me_ = await message.chat.get_member(int(me_m.id))
    if not me_.can_restrict_members:
        await pablo.edit(engine.get_string("NOT_ADMIN"))
        return
    asplit = get_text(message)
    userf = get_user(message, asplit)[0]
    if not userf:
        await pablo.edit(
            engine.get_string("TO_DO").format("Un-Mute")
        )
        return
    try:
        user = await client.get_users(userf)
    except BaseException as e:
        await pablo.edit(engine.get_string("USER_MISSING").format(e))
        return
    userz = user.id
    if userz == me_m.id:
        await pablo.edit(engine.get_string("TF_DO_IT").format("un-mute"))
        return
    try:
        await client.restrict_chat_member(
            message.chat.id, user.id, ChatPermissions(can_send_messages=True)
        )
    except BaseException as e:
        await pablo.edit(engine.get_string("FAILED_ADMIN_ACTION").format("Un-mute", e))
        return
    um = f"**#Un_Muted** \n**User :** [{user.first_name}](tg://user?id={user.id}) \n**Chat :** `{message.chat.title}`"
    await pablo.edit(um)
    log = LogIt(message)
    await log.log_msg(client, um)


@friday_on_cmd(
    ["chatinfo", "grpinfo"],
    group_only=True,
    cmd_help={"help": "Get Info Of The Chat!", "example": "{ch}chatinfo"},
)
async def owo_chat_info(client, message):
    engine = message.Engine
    s = await edit_or_reply(message, engine.get_string("PROCESSING"))
    ujwal = await client.get_chat(message.chat.id)
    peer = await client.resolve_peer(message.chat.id)
    online_ = await client.send(pyrogram.raw.functions.messages.GetOnlines(peer=peer))
    msg = "**Chat Info** \n\n"
    msg += f"**Chat-ID :** __{ujwal.id}__ \n"
    msg += f"**Verified :** __{ujwal.is_verified}__ \n"
    msg += f"**Is Scam :** __{ujwal.is_scam}__ \n"
    msg += f"**Chat Title :** __{ujwal.title}__ \n"
    msg += f"**Users Online :** __{online_.onlines}__ \n"
    if ujwal.photo:
        msg += f"**Chat DC :** __{ujwal.dc_id}__ \n"
    if ujwal.username:
        msg += f"**Chat Username :** __{ujwal.username}__ \n"
    if ujwal.description:
        msg += f"**Chat Description :** __{ujwal.description}__ \n"
    msg += f"**Chat Members Count :** __{ujwal.members_count}__ \n"
    if ujwal.photo:
        kek = await client.download_media(ujwal.photo.big_file_id)
        await client.send_photo(message.chat.id, photo=kek, caption=msg)
        await s.delete()
    else:
        await s.edit(msg)


@friday_on_cmd(
    ["purge"],
    only_if_admin=True,
    cmd_help={
        "help": "Purge All Messages Till Replied Message!",
        "example": "{ch}purge (reply to message)",
    },
)
async def purge(client, message):
    engine = message.Engine
    start_time = time.time()
    message_ids = []
    purge_len = 0
    event = await edit_or_reply(message, engine.get_string("PROCESSING"))
    me_m = client.me
    if message.chat.type in ["supergroup", "channel"]:
        me_ = await message.chat.get_member(int(me_m.id))
        if not me_.can_delete_messages:
            await event.edit(engine.get_string("NOT_ADMIN"))
            return
    if not message.reply_to_message:
        await event.edit(engine.get_string("NEEDS_REPLY").format("Message To Purge."))
        return
    async for msg in client.iter_history(
        chat_id=message.chat.id,
        offset_id=message.reply_to_message.message_id,
        reverse=True,
    ):
        if msg.message_id != message.message_id:
            purge_len += 1
            message_ids.append(msg.message_id)
            if len(message_ids) >= 100:
                await client.delete_messages(
                    chat_id=message.chat.id, message_ids=message_ids, revoke=True
                )
                message_ids.clear()
    if message_ids:
        await client.delete_messages(
            chat_id=message.chat.id, message_ids=message_ids, revoke=True
        )
    end_time = time.time()
    u_time = round(end_time - start_time)
    await event.edit(
        engine.get_string("PURGE_").format(purge_len, u_time)
    )
    await asyncio.sleep(3)
    await event.delete()


@friday_on_cmd(
    ["del"],
    cmd_help={
        "help": "Delete Replied Message!",
        "example": "{ch}del (reply to message)",
    },
)
async def delmsgs(client, message):
    engine = message.Engine
    if not message.reply_to_message:
        await message.delete()
        return
    await client.delete_messages(
        chat_id=message.chat.id,
        message_ids=[message.reply_to_message.message_id],
        revoke=True,
    )
    await message.delete()


@friday_on_cmd(
    ["setgrppic", "gpic"],
    cmd_help={
        "help": "Set Custom Group Pic, For Lazy Peoples!",
        "example": "{ch}setgrppic (reply to image)",
    },
)
async def magic_grps(client, message):
    engine = message.Engine
    msg_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    if not message.reply_to_message:
        await msg_.edit(engine.get_string("NEEDS_REPLY").format("image"))
        return
    me_ = await message.chat.get_member(int(client.me.id))
    if not me_.can_change_info:
        await msg_.edit(engine.get_string("NOT_ADMIN"))
        return
    cool = await convert_to_image(message, client)
    if not cool:
        await msg_.edit(engine.get_string("NEEDS_REPLY").format("a valid media"))
        return
    if not os.path.exists(cool):
        await msg_.edit(engine.get_string("INVALID_MEDIA"))
        return
    try:
        await client.set_chat_photo(message.chat.id, photo=cool)
    except BaseException as e:
        await msg_.edit(f"`Unable To Set Group Photo! TraceBack : {e}")
        return
    await msg_.edit(engine.get_string("DONE_"))
