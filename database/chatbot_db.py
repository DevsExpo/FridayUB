# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from database import db_x

chatbot_user_db = db_x["chatbotuserdb"]
cbb = db_x["blacklisted_users"]


async def add_chatbotuser(user_id):
    await chatbot_user_db.insert_one({"user_id": user_id})


async def rmchatbotuser(user_id):
    await chatbot_user_db.delete_one({"user_id": user_id})


async def get_all_chatbotusers():
    return [ko async for ko in chatbot_user_db.find()]


async def is_chatbotuser_in_db(user_id):
    k = await chatbot_user_db.find_one({"user_id": user_id})
    return bool(k)


async def add_blacklisted_user(user_id):
    await cbb.insert_one({"user_id": user_id})


async def rm_blacklisted_user(user_id):
    await cbb.delete_one({"user_id": user_id})


async def is_user_blacklisted(user_id):
    b = await cbb.find_one({"user_id": user_id})
    return bool(b)
