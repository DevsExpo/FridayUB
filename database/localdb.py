# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from database import db_x

ulang = db_x["UB_LANG"]


async def set_lang(lang):
    midhun = await ulang.find_one({"_id": "UB_LANG"})
    if midhun:
        if midhun['lang'] != lang:
            await ulang.update_one({"_id": "UB_LANG"}, {"$set": {"lang": lang}})
    else:
        await ulang.insert_one({"_id": "UB_LANG", "lang": lang})


async def check_lang():
    midhun = await ulang.find_one({"_id": "UB_LANG"})
    if midhun:
        return midhun['lang']
    else:
        return 'en'
