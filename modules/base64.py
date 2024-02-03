# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Base64**

๏ **Perintah:** `encode` <berikan pesan/balas pesan>
◉ **Keterangan:** Encode base64.

๏ **Perintah:** `decode` <berikan pesan/balas pesan>
◉ **Keterangan:** Decode base64.
"""

import base64

from . import ayra_cmd


@ayra_cmd(pattern="^[Ee][n][c][o][d][e]$ ?(.*)")
async def encod(e):
    match = e.pattern_match.group(1)
    if not match and e.is_reply:
        gt = await e.get_reply_message()
        if gt.text:
            match = gt.text
    if not (match or e.is_reply):
        return await e.eor("`Beri aku Sesuatu untuk Dikodekan..`")
    byt = match.encode("ascii")
    et = base64.b64encode(byt)
    atc = et.decode("ascii")
    await e.eor(f"**=>> Encoded Text :** `{match}`\n\n**=>> OUTPUT :**\n`{atc}`")


@ayra_cmd(pattern="^[Dd][e][c][o][d][e]$ ?(.*)")
async def encod(e):
    match = e.pattern_match.group(1)
    if not match and e.is_reply:
        gt = await e.get_reply_message()
        if gt.text:
            match = gt.text
    if not (match or e.is_reply):
        return await e.eor("`Beri aku Sesuatu untuk Diuraikan..`")
    byt = match.encode("ascii")
    try:
        et = base64.b64decode(byt)
        atc = et.decode("ascii")
        await e.eor(f"**=>> Decoded Text :** `{match}`\n\n**=>> OUTPUT :**\n`{atc}`")
    except Exception as p:
        await e.eor(f"**ERROR :** {str(p)}")
