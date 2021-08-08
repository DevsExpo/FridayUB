# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import io
import sys
import traceback

import requests

from main_startup.core.decorators import friday_on_cmd
from main_startup.core.startup_helpers import run_cmd
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
)

@friday_on_cmd(
    cmd=["exec", "eval"],
    ignore_errors=True,
    cmd_help={"help": "Run Python Code!", "example": '{ch}eval print("FridayUB")'},
)
async def eval(client, message):
    engine = message.Engine
    stark = await edit_or_reply(message, engine.get_string("PROCESSING"))
    cmd = get_text(message)
    if not cmd:
        await stark.edit(engine.get_string("INPUT_REQ").format("Python Code"))
        return
    if message.reply_to_message:
        message.reply_to_message.message_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success!"
    EVAL = engine.get_string("EVAL")
    final_output = EVAL.format(cmd, evaluation)
    capt = "Eval Result!" if len(cmd) >= 1023 else cmd
    await edit_or_send_as_file(final_output, stark, client, capt, "eval-result")


async def aexec(code, client, message):
    exec(
        f"async def __aexec(client, message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

@friday_on_cmd(
    cmd=["bash", "terminal"],
    ignore_errors=True,
    cmd_help={"help": "Run Bash/Terminal Command!", "example": "{ch}bash ls"},
)
async def sed_terminal(client, message):
    engine = message.Engine
    stark = await edit_or_reply(message, engine.get_string("WAIT"))
    cmd = get_text(message)
    if not cmd:
        await stark.edit(engine.get_string("INPUT_REQ").format("Bash Code"))
        return
    cmd = message.text.split(None, 1)[1]
    if message.reply_to_message:
        message.reply_to_message.message_id

    pid, err, out, ret = await run_command(cmd)
    if not out:
        out = "No OutPut!"
    friday = engine.get_string("BASH_OUT").format(cmd, pid, err, out, ret)
    await edit_or_send_as_file(friday, stark, client, cmd, "bash-result")


async def run_command(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    errors = stderr.decode()
    if not errors:
        errors = "No Errors!"
    output = stdout.decode()
    return process.pid, errors, output, process.returncode
