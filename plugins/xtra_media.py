# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import json
import logging
import os
import random
import shutil
import urllib
from re import findall

import requests
from bs4 import BeautifulSoup
from PIL import Image
from pyrogram.types import InputMediaPhoto

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, runcmd, run_in_exc
from main_startup.helper_func.gmdl import googleimagesdownload

opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36"
opener.addheaders = [("User-agent", useragent)]

sedpath = "./yandex/"
if not os.path.isdir(sedpath):
    os.makedirs(sedpath)


@friday_on_cmd(
    ["lg"],
    cmd_help={
        "help": "Mess The Animated Sticker!",
        "example": "{ch}lg (Reply To Animated Sticker)",
    },
)
async def lgo(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    if not message.reply_to_message:
        await pablo.edit(engine.get_string("NEEDS_REPLY").format("Animated Sticker"))
        return
    if not message.reply_to_message.sticker:
        await pablo.edit(engine.get_string("NEEDS_REPLY").format("Animated Sticker"))
        return
    if message.reply_to_message.sticker.mime_type != "application/x-tgsticker":
        await pablo.edit(engine.get_string("NEEDS_REPLY").format("Animated Sticker"))
        return
    lol = await message.reply_to_message.download("tgs.tgs")
    cmdo = f"lottie_convert.py {lol} json.json"
    await runcmd(cmdo)
    if not os.path.exists('json.json'):
        await pablo.edit(engine.get_string("NEEDS_REPLY").format("Animated Sticker"))
        os.remove("tgs.tgs")
        return
    with open("json.json", "r") as json:
        jsn = json.read()
    jsn = (
        jsn.replace("[1]", "[2]")
        .replace("[2]", "[3]")
        .replace("[3]", "[4]")
        .replace("[4]", "[5]")
        .replace("[5]", "[6]")
    )
    open("json.json", "w").write(jsn)
    await runcmd(f"lottie_convert.py json.json tgs.tgs")
    await client.send_sticker(message.chat.id, "tgs.tgs")
    os.remove("json.json")
    os.remove(lol)
    os.remove("tgs.tgs")
    await pablo.delete()
    
@run_in_exc    
def download_imgs_from_google(query: str, lim: int):
    response = googleimagesdownload()
    arguments = {
        "keywords": query,
        "silent_mode": True,
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory",
    }
    paths = response.download(arguments)
    path_ = paths[0][query]
    Beast = [InputMediaPhoto(str(x)) for x in path_]
    return path_, Beast

@run_in_exc
def rm_multiple_files(path_: list):
    path_ = list(path_)
    for i in path_:
        if os.path.exists(i) and os.path.isfile(i):
            os.remove(i)

@run_in_exc
def get_img_search_result(imoge: str):
    try:
        image = Image.open(imoge)
    except OSError:
        return None
    name = "okgoogle.png"
    image.save(name, "PNG")
    image.close()
    if os.path.exists(imoge):
        os.remove(imoge)
    searchUrl = "https://www.google.com/searchbyimage/upload"
    multipart = {"encoded_image": (name, open(name, "rb")), "image_content": ""}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    if os.path.exists(name):
        os.remove(name)
    if response.status_code == 400:
        return None
    return response.headers["Location"]

@friday_on_cmd(
    ["reverse"],
    cmd_help={
        "help": "Reverse Search Images / Stickers Using Google Reverse Search!",
        "example": "{ch}reverse (Reply To Image)",
    },
)
async def reverseing(client, message):
    engine = message.Engine
    input_ = get_text(message)
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    if not message.reply_to_message or not message.reply_to_message.photo:
        await pablo.edit(engine.get_string("NEEDS_REPLY").format("photo"))
        return
    imoge = await message.reply_to_message.download()
    fetchUrl = await get_img_search_result(imoge)
    if not fetchUrl:
        return await pablo.edit(engine.get_string("IMG_NOT_FOUND").format("google"))
    match = await ParseSauce(fetchUrl + "&preferences?hl=en&fg=1#languages")
    guess = match["best_guess"]
    imgspage = match["similar_images"]
    if guess and imgspage:
        await pablo.edit(engine.get_string("LOOKING_FOR_IMG").format(guess, fetchUrl))
    else:
        await pablo.edit(engine.get_string("IMG_NOT_FOUND").format("google"))
        return
    await pablo.edit(f"[{guess}]({fetchUrl})\n\n[Visually similar images]({imgspage})", disable_web_page_preview=True)
    if input_ and input_.isdigit():
        lim = int(input_)
        lst, Beast = await download_imgs_from_google(quess, lim)
        await client.send_media_group(message.chat.id, media=Beast)
        await rm_multiple_files(Beast)
@run_in_exc
def ParseSauce(googleurl):
    """Parse/Scrape the HTML code for the info we want."""
    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, "html.parser")
    results = {"similar_images": "", "best_guess": ""}
    try:
        for similar_image in soup.findAll("input", {"class": "gLFyf"}):
            url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(
                similar_image.get("value")
            )
            results["similar_images"] = url
    except BaseException:
        pass
    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
        results["best_guess"] = best_guess.get_text()
    return results


@friday_on_cmd(
    ["yandex"],
    cmd_help={
        "help": "Reverse Search Images / Stickers Using Yandex Reverse Search!",
        "example": "{ch}yandex (Reply To Image)",
    },
)
async def yandex_(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(
        message, engine.get_string("PROCESSING"))
    if not message.reply_to_message or not message.reply_to_message.photo:
        await pablo.edit(engine.get_string("NEEDS_REPLY").format("photo"))
        return
    imoge = await message.reply_to_message.download()
    filePath = imoge
    searchUrl = "https://yandex.ru/images/search"
    files = {"upfile": ("blob", open(filePath, "rb"), "image/jpeg")}
    params = {
        "rpt": "imageview",
        "format": "json",
        "request": '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}',
    }
    response = requests.post(searchUrl, params=params, files=files)
    try:
        query_string = json.loads(response.content)["blocks"][0]["params"]["url"]
    except:
        await pablo.edit(engine.get_string("IMG_NOT_FOUND").format("yandex"))
        return
    img_search_url = searchUrl + "?" + query_string
    caption = engine.get_string("YANDEX").format(img_search_url)
    await pablo.edit(caption, parse_mode="HTML", disable_web_page_preview=True)
    os.remove(imoge)


@friday_on_cmd(
    ["img", "googleimage", "image", "gi"],
    cmd_help={
        "help": "Search Images In Telegram Itself",
        "example": "{ch}img fridayuserbot",
    },
)
async def img_search(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    query = get_text(message)
    if not query:
        await pablo.edit(engine.get_string("INPUT_REQ").format("Query"))
        return
    if "|" in query:
        lim = query.split("|")[1] if (query.split("|")[1]).isdigit() else 5
    else:
        lim = 5
    lst, Beast = await download_imgs_from_google(query, lim)
    await client.send_media_group(message.chat.id, media=Beast)
    await rm_multiple_files(Beast)
    await pablo.delete()


@friday_on_cmd(
    ["waifuwrite", "wq"],
    cmd_help={
        "help": "Make Cool Stickers Using @stickerizerbot",
        "example": "{ch}wq Hi!",
    },
)
async def wow_nice(client, message):
    engine = message.Engine
    msg_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    random_s = random.randint(0, 63)
    te_t = get_text(message)
    if not te_t:
        msg_.edit(engine.get_string("INPUT_REQ").format("Text"))
        return
    text = f"#{random_s} {te_t}"
    nice = await client.get_inline_bot_results(bot="stickerizerbot", query=text)
    if message.reply_to_message:
        await client.send_inline_bot_result(
            message.chat.id,
            nice.query_id,
            nice.results[0].id,
            reply_to_message_id=message.reply_to_message.message_id,
            hide_via=True,
        )
    else:
        await client.send_inline_bot_result(
            message.chat.id, nice.query_id, nice.results[0].id, hide_via=True
        )
    await msg_.delete()
