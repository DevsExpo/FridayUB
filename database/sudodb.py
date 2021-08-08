# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from database import db_x

db_y = db_x["SUDO_USERS"]


async def add_sudo(user_id):
    cd = await db_y.find_one({"_id": "SUDO_ID"})
    if cd:
        await db_y.update_one({"_id": "SUDO_ID"}, {"$push": {"user_id": int(user_id)}})
    else:
        user_idc = [int(user_id)]
        await db_y.insert_one({"_id": "SUDO_ID", "user_id": user_idc})


async def rm_sudo(user_id):
    await db_y.update_one({"_id": "SUDO_ID"}, {"$pull": {"user_id": int(user_id)}})


async def is_user_sudo(user_id):
    sm = await db_y.find_one({"_id": "SUDO_ID"})
    if sm:
        kek = list(sm.get("user_id"))
        return user_id in kek
    else:
        return False


async def sudo_list():
    sm = await db_y.find_one({"_id": "SUDO_ID"})
    if sm:
        return [int(i) for i in sm.get("user_id")]
    else:
        return []
