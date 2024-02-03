# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Animals**

๏ **Perintah:** `dog`
◉ **Keterangan:** Mencari gambar anjing.

๏ **Perintah:** `cat`
◉ **Keterangan:** Mencari gambar kucing.
"""

import requests

from . import *


@ayra_cmd(pattern="^[Ss][Hh][Ii][Bb][Ee]$")
async def shibe(event):
    xx = await event.eor("`Processing...`")
    response = requests.get("https://shibe.online/api/shibes").json()
    if not response:
        await event.edit("**Tidak bisa menemukan gambar Anjing.**")
        return
    await event.client.send_message(entity=event.chat_id, file=response[0])
    await xx.delete()


@ayra_cmd(pattern="^[Cc][Aa][Tt]$")
async def cats(event):
    xx = await event.eor("`Processing...`")
    response = requests.get("https://shibe.online/api/cats").json()
    if not response:
        await event.edit("**Tidak bisa menemukan gambar Kucing.**")
        return
    await event.client.send_message(entity=event.chat_id, file=response[0])
    await xx.delete()
