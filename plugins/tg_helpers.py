# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
    get_user,
)


@friday_on_cmd(
    ["updatefirstname", "firstname"],
    cmd_help={
        "help": "Change Your Account First Name!",
        "example": "{ch}firstname (new firstname)",
    },
)
async def bleck_name(client, message):
    engine = message.Engine
    owo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    new_firstname = get_text(message)
    if not new_firstname:
        await owo.edit(engine.get_string("INPUT_REQ").format("Firstname"))
        return
    if len(new_firstname) > 64:
        await owo.edit(engine.get_string("NEEDS_C_INPUT"))
        return
    try:
        await client.update_profile(first_name=new_firstname)
    except BaseException as e:
        await owo.edit(
            engine.get_string("FIRST_NAME_CHANGE_FAILED").format("FirstName", e)
        )
        return
    await owo.edit(engine.get_string("FIRST_NAME_CHANGED").format("FirstName", new_firstname))


@friday_on_cmd(
    ["updatebio", "bio"],
    cmd_help={"help": "Change Your Account Bio!", "example": "{ch}bio (new bio)"},
)
async def bleck_bio(client, message):
    engine = message.Engine
    owo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    new_bio = get_text(message)
    if not new_bio:
        await owo.edit(engine.get_string("INPUT_REQ").format("Bio"))
        return
    if len(new_bio) > 70:
        await owo.edit(engine.get_string("NEEDS_C_INPUT"))
        return
    try:
        await client.update_profile(bio=new_bio)
    except BaseException as e:
        await owo.edit(engine.get_string("FIRST_NAME_CHANGE_FAILED").format("Bio", e))
        return
    await owo.edit(engine.get_string("FIRST_NAME_CHANGED").format("Bio", new_bio))


@friday_on_cmd(
    ["updateusername", "username"],
    cmd_help={
        "help": "Change Your Account UserName!",
        "example": "{ch}username (new username)",
    },
)
async def bleck_username(client, message):
    engine = message.Engine
    owo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    new_username = get_text(message)
    if not new_username:
        await owo.edit(engine.get_string("INPUT_REQ").format("Username"))
        return
    try:
        await client.update_username(new_username)
    except BaseException as e:
        await owo.edit(
            engine.get_string("FIRST_NAME_CHANGE_FAILED").format("Username", e)
        )
        return
    await owo.edit(engine.get_string("FIRST_NAME_CHANGED").format("Username", new_username))


@friday_on_cmd(
    ["updatelastname", "lastname"],
    cmd_help={
        "help": "Change Your Account Last Name!",
        "example": "{ch}lastname (new lastname)",
    },
)
async def bleck_name(client, message):
    engine = message.Engine
    owo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    new_lastname = get_text(message)
    if not new_lastname:
        await owo.edit(engine.get_string("INPUT_REQ").format("Last Name"))
        return
    if len(new_lastname) > 64:
        await owo.edit(engine.get_string("NEEDS_C_INPUT"))
        return
    try:
        await client.update_profile(last_name=new_lastname)
    except BaseException as e:
        await owo.edit(
            engine.get_string("FIRST_NAME_CHANGE_FAILED").format("LastName", e)
        )
        return
    await owo.edit(engine.get_string("FIRST_NAME_CHANGED").format("LastName", new_lastname))
    
    
@friday_on_cmd(
    ["join"],
    cmd_help={
        "help": "Join A Chat Easily.",
        "example": "{ch}join (chat link or username)",
    },
)
async def join_(client, message):
    engine = message.Engine
    owo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    input_ = get_text(message)
    if not input_:
        await owo.edit(engine.get_string("INPUT_REQ").format("Chat ID"))
        return
    try:
        await client.join_chat(input_)
    except BaseException as e:
        await owo.edit(
            engine.get_string("FAILED_TO_JOIN").format(e)
        )
        return
    await owo.edit(engine.get_string("JOINED"))

@friday_on_cmd(
    ["leave"],
    group_only=True,
    cmd_help={
        "help": "Leave Chat Easily.",
        "example": "{ch}leave",
    },
)
async def leave_(client, message):
    engine = message.Engine
    await edit_or_reply(message, "`GOODBYECRUELGROUP - *leaves*`")
    await client.leave_chat(message.chat.id)


@friday_on_cmd(
    ["updateppic", "ppic"],
    cmd_help={
        "help": "Change Your Profile Picture!",
        "example": "{ch}ppic (Reply To New Profile Picture)",
    },
)
async def bleck_pic(client, message):
    engine = message.Engine
    owo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    if not message.reply_to_message:
        await owo.edit(engine.get_string("NEEDS_REPLY").format("Video / Pic"))
        return
    if not (
        message.reply_to_message.video
        or message.reply_to_message.animation
        or message.reply_to_message.photo
    ):
        await owo.edit(engine.get_string("NEEDS_REPLY").format("Video / Pic"))
        return
    is_video = False
    if message.reply_to_message.video or message.reply_to_message.animation:
        is_video = True
    ppics = await message.reply_to_message.download()
    try:
        if is_video:
            await client.set_profile_photo(video=ppics)
        else:
            await client.set_profile_photo(photo=ppics)
    except BaseException as e:
        await owo.edit(engine.get_string("UPDATE_PIC").format(e))
        return
    await owo.edit(engine.get_string("PIC_DONE"))


@friday_on_cmd(
    ["poll"],
    group_only=True,
    cmd_help={
        "help": "Create A Poll!",
        "example": "{ch}poll Your Message | option 1, option 2, option 3",
    },
)
async def create_poll(client, message):
    engine = message.Engine
    msg = await edit_or_reply(message, engine.get_string("PROCESSING"))
    poll_ = get_text(message)
    if not poll_:
        await msg.edit(engine.get_string("REQ_POLL"))
        return
    if "|" not in poll_:
        await msg.edit(engine.get_string("A_POLL_NEEDS"))
        return
    poll_q, poll_options = poll_.split("|")
    if "," not in poll_options:
        await msg.edit(engine.get_string("A_POLL_NEEDS"))
        return
    option_s = poll_options.split(",")
    await client.send_poll(message.chat.id, question=poll_q, options=option_s)
    await msg.delete()


@friday_on_cmd(
    ["dump"],
    cmd_help={
        "help": "Get Pyrogram Message Dumbs!",
        "example": "{ch}dump",
    },
)
async def dumb_er(client, message):
    engine = message.Engine
    ow = await edit_or_reply(message, engine.get_string("PROCESSING"))
    m_sg = message.reply_to_message or message
    owo = f"{m_sg}"
    await edit_or_send_as_file(owo, ow, client, "Json-Dump", "Dump", "md")


@friday_on_cmd(
    ["purgeme"],
    cmd_help={
        "help": "Purge Your Own Message Until Given Limit!",
        "example": "{ch}purgeme 10",
    },
)
async def pur_ge_me(client, message):
    engine = message.Engine
    nice_p = await edit_or_reply(message, engine.get_string("PROCESSING"))
    msg_ids = []
    to_purge = get_text(message)
    if not to_purge:
        nice_p.edit(engine.get_string("TO_PURGE"))
        return
    if not to_purge.isdigit():
        nice_p.edit(engine.get_string("TO_PURGE"))
        return
    async for msg in client.search_messages(
        message.chat.id, query="", limit=int(to_purge), from_user="me"
    ):
        if message.message_id != msg.message_id:
            msg_ids.append(msg.message_id)
            if len(msg_ids) == 100:
                await client.delete_messages(
                    chat_id=message.chat.id, message_ids=msg_ids, revoke=True
                )
                msg_ids.clear()
    if msg_ids:
        await client.delete_messages(
            chat_id=message.chat.id, message_ids=msg_ids, revoke=True
        )
    await nice_p.edit(PURGED_MY_MSG.format(to_purge))


@friday_on_cmd(
    ["invite", "add"],
    cmd_help={
        "help": "Add Users To Channel / Groups!",
        "example": "{ch}invite @Midhun_xD @chsaiujwal @meisnub",
    },
)
async def add_user_s_to_group(client, message):
    engine = message.Engine
    mg = await edit_or_reply(message, engine.get_string("PROCESSING"))
    user_s_to_add = get_text(message)
    if not user_s_to_add:
        await mg.edit("`Give Me Users To Add! Check Help Menu For More Info!`")
        return
    user_list = user_s_to_add.split(" ")
    try:
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except BaseException as e:
        await mg.edit(engine.get_string("UNABLE_TO_ADD_USER").format(e))
        return
    await mg.edit(engine.get_string("ADDED_USER").format(len(user_list)))


@friday_on_cmd(
    ["a2c"],
    cmd_help={
        "help": "Add Users To Your Contacts!",
        "example": "{ch}a2c @Meisnub",
    },
)
async def add_user_s_to_contact(client, message):
    engine = message.Engine
    msg_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    text_ = get_text(message)
    userk = get_user(message, text_)[0]
    try:
        user_ = await client.get_users(userk)
    except BaseException as e:
        await msg_.edit(engine.get_string("USER_MISSING").format(e))
        return
    custom_name = get_text(message) or user_.first_name
    await client.add_contact(user_.id, custom_name)
    await msg_.edit(engine.get_string("ADDED_CONTACT").format(user_.first_name))
