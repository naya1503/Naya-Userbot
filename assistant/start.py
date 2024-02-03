# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.


import os
import sys
from datetime import datetime

from Ayra._misc import SUDO_M, owner_and_sudos
from Ayra.dB.asst_fns import *
from Ayra.fns.helper import inline_mention
from dotenv import load_dotenv, set_key, unset_key
from pytz import timezone as tz
from telethon import Button, events
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon.utils import get_display_name

from strings import get_string

from . import *

load_dotenv(".env")


Owner_info_msg = udB.get_key("BOT_INFO_START")
custom_info = True
if Owner_info_msg is None:
    custom_info = False
    Owner_info_msg = f"""
**Owner** - {OWNER_NAME}
**OwnerID** - `{OWNER_ID}`

**Message Forwards** - {udB.get_key("PMBOT")}

**By Kynan Join @KynanSupport**
"""

_settings = [
    [
        Button.inline("API Keys", data="cbs_apiset"),
        Button.inline("PM Bot", data="cbs_chatbot"),
    ],
    [
        Button.inline("Lainnya", data="cbs_otvars"),
        Button.inline("PM Permit", data="cbs_ppmset"),
    ],
    [Button.inline("Kembali", data="mainmenu")],
]

_start = [
    [
        Button.inline("Pengaturan ⚙️", data="setter"),
        Button.inline("Restart ♻️️", data="restart"),
    ],
    [
        Button.inline("Stats ✨", data="stat"),
        Button.inline("Broadcast 📻", data="bcast"),
    ],
    [
        Button.inline("Bahasa 🌐", data="lang"),
    ],
]

import os
import sys

heroku_api = Var.HEROKU_API
restart_counter = 0


@callback("restart", owner=True)
async def restart_callback(e):
    global restart_counter
    ok = await e.reply("`Processing...`")
    who = "bot" if e.client._bot else "user"
    udB.set_key("_RESTART", f"{who}_{e.chat_id}_{ok.id}")
    if heroku_api and restart_counter < 10:
        restart_counter += 1
    #        return await restart_callback(e)
    await bash("git pull && pip3 install -r requirements.txt")
    os.execl(sys.executable, sys.executable, "-m", "Ayra")


@asst_cmd(pattern=r"setvar (\S+)\s+(\S+)", owner=True)
async def set_env(event):
    var_name = event.pattern_match.group(1)
    var_value = event.pattern_match.group(2).replace("'", "")
    if not var_name:
        await event.reply("Berikan variable dan nilai value untuk ditetapkan!")
        return
    env_file = ".env"
    env_vars = {}

    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    env_vars[key] = value

    if var_name in env_vars:
        await event.reply(
            f"Variabel {var_name} sudah ada di file .env. Tidak dapat menambahkan variabel yang sama."
        )
        return
    set_key(env_file, var_name, var_value)
    os.environ[var_name] = var_value

    await event.reply(f"Variabel {var_name} berhasil ditambahkan.")


@asst_cmd(pattern=r"delvar (\S+)", owner=True)
async def del_env(event):
    var_name = event.pattern_match.group(1)
    if not var_name:
        await event.reply("Berikan variable untuk dihapus!")
        return
    unset_key(".env", var_name)
    if var_name in os.environ:
        del os.environ[var_name]

    await event.reply(f"Variabel {var_name} berhasil dihapus.")


@callback("ownerinfo")
async def own(event):
    msg = Owner_info_msg.format(
        mention=event.sender.mention, me=inline_mention(ayra_bot.me)
    )
    if custom_info:
        msg += "\n\n• Powered by **@kynansupport**"
    await event.edit(
        msg,
        buttons=[Button.inline("Tutup", data="closeit")],
        link_preview=False,
    )


@callback("closeit")
async def closet(lol):
    try:
        await lol.delete()
    except MessageDeleteForbiddenError:
        await lol.answer("MESSAGE_TOO_OLD", alert=True)


@asst_cmd(pattern="start( (.*)|$)", forwards=False, func=lambda x: not x.is_group)
async def ayra(event):
    args = event.pattern_match.group(1).strip()
    if not is_added(event.sender_id) and event.sender_id not in owner_and_sudos():
        add_user(event.sender_id)
        kak_uiw = udB.get_key("OFF_START_LOG")
        if not kak_uiw or kak_uiw != True:
            msg = f"{inline_mention(event.sender)} `[{event.sender_id}]` Ada pesan dari [Assistant bot](@{asst.me.username})."
            buttons = [[Button.inline("Info", "itkkstyo")]]
            if event.sender.username:
                buttons[0].append(
                    Button.mention(
                        "User", await event.client.get_input_entity(event.sender_id)
                    )
                )
            await event.client.send_message(
                udB.get_key("LOG_CHANNEL"), msg, buttons=buttons
            )
    if event.sender_id not in SUDO_M.fullsudos:
        ok = ""
        me = inline_mention(ayra_bot.me)
        mention = inline_mention(event.sender)
        if args and args != "set":
            await get_stored_file(event, args)
        if not udB.get_key("STARTMSG"):
            if udB.get_key("PMBOT"):
                ok = "Anda dapat menghubungi Owner saya menggunakan bot ini!!\n\nKirim Pesan Anda, saya akan Kirim ke Owner."
            await event.reply(
                f"Hey {mention}, Aku Adalah Ayra Asissten {me}!\n\n{ok}",
                file=udB.get_key("STARTMEDIA"),
                buttons=(
                    [Button.inline("Info.", data="ownerinfo")]
                    if Owner_info_msg
                    else None
                ),
            )
        else:
            await event.reply(
                udB.get_key("STARTMSG").format(me=me, mention=mention),
                file=udB.get_key("STARTMEDIA"),
                buttons=(
                    [Button.inline("Info.", data="ownerinfo")]
                    if Owner_info_msg
                    else None
                ),
            )
    else:
        name = get_display_name(event.sender)
        if args == "set":
            await event.reply(
                "Pilih dari opsi di bawah ini",
                buttons=_settings,
            )
        elif args:
            await get_stored_file(event, args)
        else:
            await event.reply(
                get_string("ast_3").format(name),
                buttons=_start,
            )


@callback("itkkstyo", owner=True)
async def ekekdhdb(e):
    text = f"When New Visitor will visit your Assistant Bot. You will get this log message!\n\nTo Disable : {HNDLR}setdb OFF_START_LOG True"
    await e.answer(text, alert=True)


@callback("mainmenu", owner=True, func=lambda x: not x.is_group)
async def ayra(event):
    await event.edit(
        get_string("ast_3").format(OWNER_NAME),
        buttons=_start,
    )


@callback("stat", owner=True)
async def botstat(event):
    ok = len(get_all_users("BOT_USERS"))
    msg = """Naya-Userbot Assistant - Stats
Total Users - {}""".format(
        ok,
    )
    await event.answer(msg, cache_time=0, alert=True)


@callback("bcast", owner=True)
async def bdcast(event):
    ok = get_all_users("BOT_USERS")
    await event.edit(f"• Broadcast to {len(ok)} users.")
    async with event.client.conversation(OWNER_ID) as conv:
        await conv.send_message(
            "Enter your broadcast message.\nUse /cancel to stop the broadcast.",
        )
        response = await conv.get_response()
        if response.message == "/cancel":
            return await conv.send_message("Cancelled!!")
        success = 0
        fail = 0
        await conv.send_message(f"Starting a broadcast to {len(ok)} users...")
        start = datetime.now()
        for i in ok:
            try:
                await asst.send_message(int(i), response)
                success += 1
            except BaseException:
                fail += 1
        end = datetime.now()
        time_taken = (end - start).seconds
        await conv.send_message(
            f"""
**Broadcast completed in {time_taken} seconds.**
Total Users in Bot - {len(ok)}
**Sent to** : `{success} users.`
**Failed for** : `{fail} user(s).`""",
        )


@callback("setter", owner=True)
async def setting(event):
    await event.edit(
        "Silakan pilih pengaturan yang anda inginkan.",
        buttons=_settings,
    )


@callback("tz", owner=True)
async def timezone_(event):
    await event.delete()
    pru = event.sender_id
    var = "TIMEZONE"
    name = "Timezone"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "Send Your TimeZone From This List [Check From Here](http://www.timezoneconverter.com/cgi-bin/findzone.tzc)"
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Cancelled!!",
                buttons=get_back_button("mainmenu"),
            )
        try:
            tz(themssg)
            await setit(event, var, themssg)
            await conv.send_message(
                f"{name} changed to {themssg}\n",
                buttons=get_back_button("mainmenu"),
            )
        except BaseException:
            await conv.send_message(
                "Wrong TimeZone, Try again",
                buttons=get_back_button("mainmenu"),
            )
