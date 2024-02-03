# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Sosmed**

๏ **Perintah:** `sosmed` <berikan link/balas link>
◉ **Keterangan:** Download Video Facebook, Youtube, Tiktok, Instagram, Twitter.
"""


try:
    import cv2
except ImportError:
    cv2 = None

try:
    from htmlwebshot import WebShot
except ImportError:
    WebShot = None
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import *


@ayra_cmd(pattern="[Ss][o][s][m][e][d](?: |$)(.*)")
async def _(event):
    if xxnx := event.pattern_match.group(1):
        d_link = xxnx
    elif event.is_reply:
        d_link = await event.get_reply_message()
    else:
        return await eod(
            event,
            "**Berikan Link Pesan atau Reply Link Untuk di Download**",
        )
    xx = await eor(event, "`Processing...`")
    chat = "@thisvidbot"
    async with event.client.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            r = await conv.get_response()
            msg = await conv.send_message(d_link)
            details = await conv.get_response()
            video = await conv.get_response()
            text = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            msg_start = await conv.send_message("/start")
            r = await conv.get_response()
            msg = await conv.send_message(d_link)
            details = await conv.get_response()
            video = await conv.get_response()
            text = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        await event.client.send_file(
            event.chat_id,
            video,
            caption=f"**Upload By: {inline_mention(event.sender)}**",
        )
        await event.client.delete_messages(
            conv.chat_id, [msg_start.id, r.id, msg.id, details.id, video.id, text.id]
        )
        await xx.delete()
