# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Spam**

๏ **Perintah:** `spam` <jumlah> <berikan pesan/balas pesan>
◉ **Keterangan:** Lakukan spam, batas saat ini adalah dari 1 hingga 99.

๏ **Perintah:** `bspam` <jumlah> <berikan pesan/balas pesan>
◉ **Keterangan:** Lakukan spam diatas 100 di obrolan.

๏ **Perintah:** `dspam` <waktu delay><jumlah><balas pesan>
◉ **Keterangan:** Delay spam dengan waktu dan jumlah tertentu.

๏ **Perintah:** `tspam` <berikan pesan>
◉ **Keterangan:** Spam PerKarakter.
"""

import asyncio

from . import *


@ayra_cmd(pattern="[tT]spam", fullsudo=False)
async def tmeme(e):
    tspam = str(e.text[7:])
    message = tspam.replace(" ", "")
    for letter in message:
        await e.respond(letter)
    await e.delete()


@ayra_cmd(pattern="[sS]pam", fullsudo=False)
async def spammer(e):
    message = e.text
    if e.reply_to:
        if len(message.split()) < 2:
            return await eod(e, "`Gunakan dalam Format yang Tepat`")
        spam_message = await e.get_reply_message()
    elif len(message.split()) < 3:
        return await eod(e, "`Membalas Pesan atau berikan beberapa Teks ..`")
    else:
        spam_message = message.split(maxsplit=2)[2]
    counter = message.split()[1]
    try:
        counter = int(counter)
        if counter >= 100:
            return await eod(e, "`Gunakan bigspam`")
    except BaseException:
        return await eod(e, "`Gunakan dalam Format yang Tepat`")

    tasks = [asyncio.create_task(e.respond(spam_message)) for _ in range(counter)]
    await asyncio.wait(tasks)
    await e.delete()


@ayra_cmd(pattern="[bB]spam", fullsudo=True)
async def bigspam(e):
    message = e.text
    if e.reply_to:
        if len(message.split()) < 2:
            return await eod(e, "`Gunakan dalam Format yang Tepat`")
        spam_message = await e.get_reply_message()
    elif len(message.split()) < 3:
        return await eod(e, "`Membalas Pesan atau Memberikan beberapa Teks ..`")
    else:
        spam_message = message.split(maxsplit=2)[2]
    counter = message.split()[1]
    try:
        counter = int(counter)
    except BaseException:
        return await eod(e, "`Gunakan dalam Format yang Tepat`")
    await asyncio.wait([e.respond(spam_message) for _ in range(counter)])
    await e.delete()


@ayra_cmd(pattern="[dD]spam?(.*)", fullsudo=False)
async def delayspammer(e):
    try:
        args = e.text.split(" ", 3)
        delay = float(args[1])
        count = int(args[2])
        spam_message = await e.get_reply_message() if e.reply_to else str(args[3])
    except BaseException:
        return await e.edit(
            f"**Penggunaan :** {HNDLR} dspam <waktu delay> <jumlah> <balas pesan>"
        )
    await e.delete()
    try:
        for _ in range(count):
            await e.respond(spam_message)
            await asyncio.sleep(delay)
    except Exception as u:
        await e.respond(f"**Error :** `{u}`")
