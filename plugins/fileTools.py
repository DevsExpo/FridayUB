# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import logging
import os
import pathlib
import shutil
import time
import uuid

import img2pdf
from fsplit.filesplit import Filesplit

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    get_text,
    humanbytes,
    progress,
)


@friday_on_cmd(
    ["chnnlzip", "channelzip"],
    cmd_help={
        "help": "Zips All The Messages/Files/Everything From A Channel/Group",
        "example": "{ch}chnnlzip",
    },
)
async def chnnlzip(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("FILE_TOOLS_1"))
    rndm = uuid.uuid4().hex
    un = get_text(message)
    dirz = f"./{rndm}/"
    media_count = 0
    text_count = 0
    os.makedirs(dirz)
    chnnl = un or message.chat.id
    async for msg in client.iter_history(chnnl):
        if msg.sticker:
            rndmname = uuid.uuid4().hex
            if msg.sticker.mime_type == "application/x-tgsticker":
                file_name = os.path.join(dirz + rndmname + ".tgs")
            else:
                file_name = os.path.join(dirz + rndmname + ".wepb")
            try:
                await msg.download(file_name=file_name)
            except Exception as e:
                logging.info(e)
        elif msg.media:
            media_count += 1
            try:
                await msg.download(file_name=dirz)
            except Exception as e:
                logging.info(e)
        elif msg.text:
            text_count += 1
            f = open(os.path.join(dirz + f"{chnnl}.txt"), "a")
            f.write(f"[{msg.date}] - {msg.text} \n\n")
    total = text_count + media_count
    await pablo.edit(
        engine.get_string("FILE_TOOLS_2").format(total, media_count, text_count)
    )
    shutil.make_archive(str(f"{chnnl}_ZippedByFridayUB"), "zip", dirz)
    await pablo.edit("`Zipped! Uploading Now!`")
    zip_name = f"{chnnl}_ZippedByFridayUB.zip"
    siz_e = os.stat(zip_name).st_size
    list_ = []
    if siz_e > 2040108421:
        await pablo.edit(
            engine.get_string("FILE_TOOLS_3")
        )
        fs = Filesplit()
        if not os.path.exists(f"./splitted_{chnnl}_{rndm}"):
            os.makedirs(f"./splitted_{chnnl}_{rndm}")
        fs.split(
            file=zip_name,
            split_size=2040108421,
            output_dir=f"./splitted_{chnnl}_{rndm}",
        )
        file_list(f"./splitted_{chnnl}_{rndm}", list_)
        for oof in list_:
            if oof == "fs_manifest.csv":
                return
            await client.send_document(
                message.chat.id,
                oof,
                caption=f"**Total :** `{total}` \n**Total Media :** `{media_count}` \n**Total Text :** `{text_count}`",
            )
        shutil.rmtree(dirz)
        shutil.rmtree(f"./splitted_{chnnl}_{rndm}")
        if os.path.exists(zip_name):
            os.remove(zip_name)
        await pablo.delete()
        return
    await client.send_document(
        message.chat.id,
        zip_name,
        caption=f"**Total :** `{total}` \n**Total Media :** `{media_count}` \n**Total Text :** `{text_count}`",
    )
    os.remove(zip_name)
    shutil.rmtree(dirz)
    await pablo.delete()


def file_list(path, lisT):
    pathlib.Path(path)
    for filepath in pathlib.Path(path).glob("**/*"):
        lisT.append(filepath.absolute())
    return lisT


@friday_on_cmd(
    ["pdf", "channelpdf"],
    cmd_help={
        "help": "Makes A PDF With All Images In Group/Channel!",
        "example": "{ch}pdf",
    },
)
async def chnnlpdf(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("FILE_TOOLS_1"))
    rndm = uuid.uuid4().hex
    un = get_text(message)
    dirz = f"./{rndm}/"
    photo_count = 0
    os.makedirs(dirz)
    chnnl = un or message.chat.id
    images_path = []
    async for msg in client.iter_history(chnnl):
        if msg.photo:
            rndmname = uuid.uuid4().hex
            file_name = os.path.join(dirz + rndmname + ".jpg")
            photo_count += 1
            try:
                file_path = await msg.download(file_name=file_name)
                images_path.append(file_path)
            except Exception as e:
                logging.info(f"Failed To Download - {e}")
    if not images_path:
        await pablo.edit(engine.get_string("IMAGE_NOT_FOUND").format("This Chat"))
        shutil.rmtree(dirz)
        return
    with open("imagetopdf@fridayot.pdf", "wb") as f:
        f.write(img2pdf.convert(images_path))
    capt = f"**CONVERTED** \n**Total Images :** `{len(images_path)}` \n**Channel / Group :** `{chnnl}`"
    await client.send_document(message.chat.id, "imagetopdf@fridayot.pdf", caption=capt)
    os.remove("imagetopdf@fridayot.pdf")
    shutil.rmtree(dirz)
    await pablo.delete()


@friday_on_cmd(
    ["Download"],
    cmd_help={
        "help": "Downloads Replied File To Local Storage!",
        "example": "{ch}download (replying-to-file)",
    },
)
async def Download(client, message):
    s_time = time.time()
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    if not message.reply_to_message:
        await pablo.edit(engine.get_string("REPLY_MSG"))
        return
    if not message.reply_to_message.media:
        await pablo.edit(engine.get_string("REPLY_MSG"))
        return
    c_time = time.time()
    Escobar = await message.reply_to_message.download(
        progress=progress, progress_args=(pablo, c_time, f"`Downloading This File!`")
    )
    e_time = time.time()
    dl_time = round(s_time - e_time)
    await pablo.edit(engine.get_string("FILE_TOOLS_5").format(Escobar, dl_time))


@friday_on_cmd(
    ["setthumb"],
    cmd_help={
        "help": "Set Thumbnail For Upload Files!",
        "example": "{ch}setthumb (Replying to thumbnail)",
    },
)
async def st(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    if not message.reply_to_message:
        await pablo.edit(engine.get_string("FILE_TOOLS_6"))
        return
    if not message.reply_to_message.photo:
        await pablo.edit(engine.get_string("FILE_TOOLS_6"))
        return
    await message.reply_to_message.download(file_name="./main_startup/Cache/thumb.jpg")
    await pablo.edit(
        engine.get_string("FILE_TOOLS_7")
    )


image_ext = tuple([".jpg", ".png", ".jpeg"])
vid_ext = tuple([".mp4", ".mkv"])
sticker_ext = tuple([".wepb", ".tgs"])
song_ext = tuple([".mp3", ".wav", ".m4a"])


@friday_on_cmd(
    ["Upload"],
    cmd_help={
        "help": "Upload Internal File!",
        "example": "{ch}upload (local file path)",
    },
)
async def upload(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    file = get_text(message)
    c_time = time.time()
    if not file:
        await pablo.edit(
            engine.get_string("INPUT_REQ").format("File Path")
            )
        return
    if not os.path.exists(file):
        await pablo.edit(engine.get_string("F_404"))
        return
    file_name = os.path.basename(file)
    send_as_thumb = bool(os.path.exists("./main_startup/Cache/thumb.jpg"))
    size = os.stat(file).st_size
    if file.endswith(image_ext):
        # assume its image file
        capt = f"File Name : `{file_name}` \nFile Size : `{humanbytes(size)}` \nFile Type : `Image (Guessed)`"
        await client.send_photo(
            message.chat.id,
            file,
            caption=capt,
            progress=progress,
            progress_args=(pablo, c_time, f"`Uploading {file_name}!`", file_name),
        )
    elif file.endswith(vid_ext):
        capt = f"File Name : `{file_name}` \nFile Size : `{humanbytes(size)}` \nFile Type : `Video (Guessed)`"
        if send_as_thumb:
            await client.send_video(
                message.chat.id,
                file,
                thumb="./main_startup/Cache/thumb.jpg",
                caption=capt,
                progress=progress,
                progress_args=(pablo, c_time, f"`Uploading {file_name}!`", file_name),
            )
        else:
            await client.send_video(
                message.chat.id,
                file,
                caption=capt,
                progress=progress,
                progress_args=(pablo, c_time, f"`Uploading {file_name}!`", file_name),
            )
    elif file.endswith(".gif"):
        capt = f"File Name : `{file_name}` \nFile Size : `{humanbytes(size)}` \nFile Type : `Gif (Guessed)`"
        if send_as_thumb:
            await client.send_animation(
                message.chat.id,
                file,
                thumb="./main_startup/Cache/thumb.jpg",
                caption=capt,
                progress=progress,
                progress_args=(pablo, c_time, f"`Uploading {file_name}!`", file_name),
            )
        else:
            await client.send_animation(
                message.chat.id,
                file,
                caption=capt,
                progress=progress,
                progress_args=(pablo, c_time, f"`Uploading {file_name}!`", file_name),
            )
    elif file.endswith(song_ext):
        capt = f"File Name : `{file_name}` \nFile Size : `{humanbytes(size)}` \nFile Type : `Audio (Guessed)`"
        if send_as_thumb:
            await client.send_audio(
                message.chat.id,
                file,
                thumb="./main_startup/Cache/thumb.jpg",
                caption=capt,
                progress=progress,
                progress_args=(pablo, c_time, f"`Uploading {file_name}!`", file_name),
            )
        else:
            await client.send_audio(
                message.chat.id,
                file,
                caption=capt,
                progress=progress,
                progress_args=(pablo, c_time, f"`Uploading {file_name}!`", file_name),
            )
    elif file.endswith(sticker_ext):
        await client.send_sticker(
            message.chat.id,
            file,
            progress=progress,
            progress_args=(pablo, c_time, f"`Uploading {file_name}!`", file_name),
        )
    else:
        capt = f"File Name : `{file_name}` \nFile Size : `{humanbytes(size)}` \nFile Type : `Document (Guessed)`"
        if send_as_thumb:
            await client.send_document(
                message.chat.id,
                file,
                thumb="./main_startup/Cache/thumb.jpg",
                caption=capt,
                progress=progress,
                progress_args=(pablo, c_time, f"`Uploading {file_name}!`", file_name),
            )
        else:
            await client.send_document(
                message.chat.id,
                file,
                caption=capt,
                progress=progress,
                progress_args=(pablo, c_time, f"`Uploading {file_name}!`", file_name),
            )
    await pablo.delete()
