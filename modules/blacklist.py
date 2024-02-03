# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

"""
✘ **Bantuan Untuk Blacklist**

๏ **Perintah:** `bl` <kata>
◉ **Keterangan:** Daftar hitam kan kata didalam grup.

๏ **Perintah:** `wl` <kata>
◉ **Keterangan:** Hapus kata dari daftar hitam.

๏ **Perintah:** `listbl`
◉ **Keterangan:** Lihat Semua Daftar Kata Terlarang .
"""


from Ayra.dB.blacklist_db import (add_blacklist, get_blacklist, list_blacklist,
                                  rem_blacklist)

from . import ayra_bot, ayra_cmd, events, get_string, udB


@ayra_cmd(pattern="^[Bb][l]( (.*)|$)")
async def af(e):
    direp = await e.get_reply_message()
    teks = direp.text if direp else e.pattern_match.group(3)
    chat = e.chat_id
    if not teks:
        return await e.eor(get_string("blk_1"), time=5)
    kata = teks.split()
    for x in kata:
        add_blacklist(int(chat), x.lower())
    ayra_bot.add_handler(blacklist, events.NewMessage(incoming=True))
    await e.eor(get_string("blk_2").format(x))


@ayra_cmd(pattern="^[Ww][l]( (.*)|$)")
async def rf(e):
    teks = e.pattern_match.group(2)
    chat = e.chat_id
    if not teks:
        return await e.eor(get_string("blk_3"), time=5)
    kata = teks.split()
    for x in kata:
        rem_blacklist(int(chat), x)
    await e.eor(get_string("blk_4").format(x))


@ayra_cmd(pattern="^[Ll][i][s][t][b][l]")
async def lsnote(e):
    if x := list_blacklist(e.chat_id):
        sd = get_string("blk_5")
        return await e.eor(sd + x)
    await e.eor(get_string("blk_6"))


async def blacklist(e):
    if x := get_blacklist(e.chat_id):
        for z in e.text.lower().split():
            for zz in x:
                if z == zz:
                    try:
                        await e.delete()
                        break
                    except BaseException:
                        break


if udB.get_key("BLACKLIST_DB"):
    ayra_bot.add_handler(blacklist, events.NewMessage(incoming=True))
