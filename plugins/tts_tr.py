# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import os
import time
import gtts
import requests
from googletrans import LANGUAGES, Translator
from gtts import gTTS
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from langdetect import detect

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text, run_in_exc

@run_in_exc
def tr(text, lang):
    translator = Translator()
    if not LANGUAGES.get(lang):
        return None, None, None
    translated = translator.translate(text, dest=lang, src='auto')
    source_lan = LANGUAGES.get(translated.src.lower())
    transl_lan = LANGUAGES.get(translated.dest.lower())
    return source_lan, transl_lan, translated

@run_in_exc
def parse_tts(text_, lang, file):
    tts = gTTS(text_, lang=lang)
    tts.save(file)
    try:
        dec_s = detect(text_)
    except:
        dec_s = "unknown"
    duration = 0
    metadata = extractMetadata(createParser(file))
    if metadata and metadata.has("duration"):
        duration = metadata.get("duration").seconds
    return file, dec_s, duration
    
    
@friday_on_cmd(
    ["tts", "voice", "texttospeech"],
    cmd_help={
        "help": "Convert Text To Speech!",
        "example": "{ch}voice (reply to text) (Language code)",
    },
)
async def gibspeech(client, message):
    engine = message.Engine
    stime = time.time()
    event = await edit_or_reply(message, engine.get_string("PROCESSING"))
    ttslang = get_text(message)
    if not message.reply_to_message:
        await event.edit(engine.get_string("NEEDS_REPLY").format("Convert To Speech"))
        return
    if not message.reply_to_message.text:
        await event.edit(engine.get_string("NEEDS_REPLY").format("Convert To Speech"))
        return
    text = message.reply_to_message.text
    language = "en" if not ttslang else ttslang
    kk = gtts.lang.tts_langs()
    if not kk.get(language):
        await event.edit(engine.get_string("UNSUPPORTED").format("Corrent Language Code"))
        return
    await client.send_chat_action(message.chat.id, "record_audio")
    file = f"{kk.get(language)}.ogg"
    file, dec_s, duration = await parse_tts(text, language, file)
    etime = time.time()
    hmm_time = round(etime - stime)
    owoc = f"**TTS** \n**Detected Text Language :** `{dec_s.capitalize()}` \n**Speech Text :** `{kk.get(language)}` \n**Time Taken :** `{hmm_time}s` \n__Powered By @FridayOT__"
    await message.reply_audio(
        audio=file, caption=owoc, duration=duration
    )
    await client.send_chat_action(message.chat.id, action="cancel")
    if os.path.exists(file):
        os.remove(file)
    await event.delete()


@friday_on_cmd(
    ["tr", "translate"],
    cmd_help={
        "help": "Translate text from one Language To Another!",
        "example": "{ch}tr (reply to text) (language-code)",
    },
)
async def tr_pls(client, message):
    engine = message.Engine
    event = await edit_or_reply(message, engine.get_string("PROCESSING"))
    lang = get_text(message)
    if not lang:
        lang = "en"
    if not message.reply_to_message:
        await event.edit(engine.get_string("NEEDS_REPLY").format("Translate It"))
        return
    if not message.reply_to_message.text:
        await event.edit(engine.get_string("NEEDS_REPLY").format("Translate It"))
        return
    text = message.reply_to_message.text
    source_lan, transl_lan, translated = await tr(text, lang)
    if not source_lan:
        return await event.edit(engine.get_string("NEEDS_C_INPUT"))
    tr_text = f"""<b>Source ({source_lan.capitalize()})</b>
<b>Translation ({transl_lan.capitalize()})</b>:
<code>{translated}</code>"""
    if len(tr_text) >= 4096:
        url = "https://del.dog/documents"
        r = requests.post(url, data=translated.encode("UTF-8")).json()
        url2 = f"https://del.dog/{r['key']}"
        tr_text = (
            engine.get_string("TOO_BIG").format(url2)
        )
    await event.edit(tr_text)
