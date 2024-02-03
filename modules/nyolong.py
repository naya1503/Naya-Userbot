# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Pinterest**

๏ **Perintah:** `copy` <link>
◉ **Keterangan:** Colong media dari ch private.

๏ **Perintah:** `curi` <balas pesan>
◉ **Keterangan:** Curi pap timer.
"""

from telethon.errors.rpcerrorlist import (ChatForwardsRestrictedError,
                                          MediaEmptyError)

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from htmlwebshot import WebShot
except ImportError:
    WebShot = None

from . import *

LOG_CHANNEL = udB.get_key("LOG_CHANNEL")


@ayra_cmd(pattern="[cC]opy(?: |$)(.*)")
async def get_restriced_msg(event):
    match = event.pattern_match.group(1).strip()
    if not match:
        await event.eor("`Please provide a link!`", time=5)
        return
    xx = await event.eor(get_string("com_1"))
    chat, msg = get_chat_and_msgid(match)
    if not (chat and msg):
        return await event.eor(
            f"{get_string('gms_1')}!\nEg: `https://t.me/sfsdf/3 or `https://t.me/c/afdffd/3`"
        )
    try:
        message = await event.client.get_messages(chat, ids=msg)
    except BaseException as er:
        return await event.eor(f"**ERROR**\n`{er}`")
    try:
        await event.client.send_message(event.chat_id, message)
        await xx.try_delete()
        return
    except ChatForwardsRestrictedError:
        pass
    except MediaEmptyError:
        pass
    if message.media and message.document:
        thumb = None
        if message.document.thumbs:
            thumb = await message.download_media(thumb=-1)
        media = await event.client.download_media(message.document)
        await xx.edit("`Uploading...`")
        uploaded = await event.client.send_file(
            event.chat_id, file=media, caption="**Done.**"
        )
        await xx.delete()
        if thumb:
            os.remove(thumb)


@ayra_cmd(pattern=r"[Cc]uri(?: |$)(.*)")
async def pencuri(event):
    dia = await event.get_reply_message()
    botlog = LOG_CHANNEL
    xx = await event.eor("`...`", time=2)
    if not dia:
        return
    dia.text or None
    pap = await event.client.download_media(dia)
    try:
        await event.client.send_file(botlog, pap, caption="Pap nya...")
    except Exception as e:
        print(e)
