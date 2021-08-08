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
import requests
import wget
from youtube_dl import YoutubeDL
from youtubesearchpython import SearchVideos
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.assistant_helpers import _dl
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, progress, humanbytes, run_in_exc, time_formatter
import threading
from concurrent.futures import ThreadPoolExecutor
from pyrogram.errors import FloodWait, MessageNotModified

def edit_msg(client, message, to_edit):
    try:
        client.loop.create_task(message.edit(to_edit))
    except MessageNotModified:
        pass
    except FloodWait as e:
        client.loop.create_task(asyncio.sleep(e.x))
    except TypeError:
        pass
    
def download_progress_hook(d, message, client):
    if d['status'] == 'downloading':
        current = d.get("_downloaded_bytes_str") or humanbytes(int(d.get("downloaded_bytes", 1)))
        total = d.get("_total_bytes_str") or d.get("_total_bytes_estimate_str")
        file_name = d.get("filename")
        eta = d.get('_eta_str', "N/A")
        percent = d.get("_percent_str", "N/A")
        speed = d.get("_speed_str", "N/A")
        to_edit = f"<b><u>Downloading File</b></u> \n<b>File Name :</b> <code>{file_name}</code> \n<b>File Size :</b> <code>{total}</code> \n<b>Speed :</b> <code>{speed}</code> \n<b>ETA :</b> <code>{eta}</code> \n<i>Download {current} out of {total}</i> (__{percent}__)"
        threading.Thread(target=edit_msg, args=(client, message, to_edit)).start()

@run_in_exc
def yt_dl(url, client, message, type_):
    if type_ == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "progress_hooks": [lambda d: download_progress_hook(d, message, client)],
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
    else:
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "progress_hooks": [lambda d: download_progress_hook(d, message, client)],
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
    with YoutubeDL(opts) as ytdl:
        ytdl_data = ytdl.extract_info(url, download=True)
    file_name = f"{ytdl_data['id']}.mp3" if type_ == "audio" else f"{ytdl_data['id']}.mp4"
    print(file_name)
    return file_name, ytdl_data


@friday_on_cmd(
    ["yt", "ytdl"],
    cmd_help={
        "help": "Download YouTube Videos / Audio just with name!",
        "example": "{ch}yt (video name OR link)|audio if audio else video",
    },
)
async def yt_vid(client, message):
    input_str = get_text(message)
    engine = message.Engine
    type_ = "video"
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    if not input_str:
        await pablo.edit(
            engine.get_string("INPUT_REQ").format("Query")
        )
        return
    _m = ('http://', 'https://')
    if "|" in input_str:
        input_str = input_str.strip()
        input_str, type_ = input_str.split("|")
    if type_ not in ['audio', 'video']:
        return await pablo.edit(engine.get_string("NEEDS_C_INPUT"))
    if input_str.startswith(_m):
        url = input_str
    else:
        await pablo.edit(engine.get_string("GETTING_RESULTS").format(input_str))
        search = SearchVideos(str(input_str), offset=1, mode="dict", max_results=1)
        if not search:
            return await pablo.edit(engine.get_string("NO_RESULTS").format(input_str))
        rt = search.result()
        result_s = rt["search_result"]
        url = result_s[0]["link"]
    try:
        yt_file, yt_data = await yt_dl(url, client, message, type_)
    except Exception as e:
        return await pablo.edit(engine.get_string("YTDL_FAILED").format(e))
    vid_title = yt_data['title']
    uploade_r = yt_data['uploader']
    yt_id = yt_data['id']
    msg = message.reply_to_message or message 
    thumb_url = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
    thumb = await _dl(thumb_url)
    caption = f"**{type_.title()} Name ➠** `{vid_title}` \n**Requested For ➠** `{input_str}` \n**Channel ➠** `{uploade_r}` \n**Link ➠** `{url}`"
    c_time = time.time()
    if type_ == "video":
        await msg.reply_video(
            yt_file,
            duration=int(yt_data["duration"]),
            thumb=thumb,
            caption=caption,
            supports_streaming=True,
            progress=progress,
            progress_args=(
                pablo,
                c_time,
                f"`Uploading Downloaded Youtube File.`",
                str(yt_file),
            ),
        )
    else:
        await msg.reply_audio(
            yt_file,
            duration=int(yt_data["duration"]),
            title=str(yt_data["title"]),
            performer=uploade_r,
            thumb=thumb,
            caption=caption,
            progress=progress,
            progress_args=(
                pablo,
                c_time,
                f"`Uploading Downloaded Youtube File.`",
                str(yt_file),
            ),
        )
    await pablo.delete()
    for files in (thumb, yt_file):
        if files and os.path.exists(files):
            os.remove(files)