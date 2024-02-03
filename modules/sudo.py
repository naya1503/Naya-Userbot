# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Sudo**

๏ **Perintah:** `addsudo`
◉ **Keterangan:** Tambahkan Pengguna Sudo dengan membalas ke pengguna atau menggunakan <spasi> userid yang terpisah

๏ **Perintah:** `delsudo`
◉ **Keterangan:** Hapus Pengguna Sudo dengan membalas ke pengguna atau menggunakan <spasi> userid yang terpisah

๏ **Perintah:** `listsudo`
◉ **Keterangan:** Daftar semua pengguna sudo.
"""

from Ayra._misc import sudoers
from telethon.tl.types import User

from . import ayra_bot, ayra_cmd, get_string, inline_mention, udB


@ayra_cmd(pattern="[Aa][d][d][s][u][d][o]( (.*)|$)", fullsudo=False)
async def _(ayra):
    inputs = ayra.pattern_match.group(1).strip()
    if ayra.reply_to_msg_id:
        replied_to = await ayra.get_reply_message()
        id = replied_to.sender_id
        name = await replied_to.get_sender()
    elif inputs:
        try:
            id = await ayra.client.parse_id(inputs)
        except ValueError:
            try:
                id = int(inputs)
            except ValueError:
                id = inputs
        try:
            name = await ayra.client.get_entity(int(id))
        except BaseException:
            name = None
    elif ayra.is_private:
        id = ayra.chat_id
        name = await ayra.get_chat()
    else:
        return await ayra.eor(get_string("sudo_1"), time=5)
    if name and isinstance(name, User) and (name.bot or name.verified):
        return await ayra.eor(get_string("sudo_4"))
    name = inline_mention(name) if name else f"`{id}`"
    if id == ayra_bot.uid:
        mmm = get_string("sudo_2")
    elif id in sudoers():
        mmm = f"{name} `sudah menjadi Pengguna SUDO ...`"
    else:
        udB.set_key("SUDO", "True")
        key = sudoers()
        key.append(id)
        udB.set_key("SUDOS", key)
        mmm = f"**Ditambahkan** {name} **sebagai Pengguna SUDO**"
    await ayra.eor(mmm, time=5)


@ayra_cmd(pattern="[Dd][e][l][s][u][d][o]( (.*)|$)", fullsudo=False)
async def _(ayra):
    inputs = ayra.pattern_match.group(1).strip()
    if ayra.reply_to_msg_id:
        replied_to = await ayra.get_reply_message()
        id = replied_to.sender_id
        name = await replied_to.get_sender()
    elif inputs:
        try:
            id = await ayra.client.parse_id(inputs)
        except ValueError:
            try:
                id = int(inputs)
            except ValueError:
                id = inputs
        try:
            name = await ayra.client.get_entity(int(id))
        except BaseException:
            name = None
    elif ayra.is_private:
        id = ayra.chat_id
        name = await ayra.get_chat()
    else:
        return await ayra.eor(get_string("sudo_1"), time=5)
    name = inline_mention(name) if name else f"`{id}`"
    if id not in sudoers():
        mmm = f"{name} `bukan Pengguna SUDO ...`"
    else:
        key = sudoers()
        key.remove(id)
        udB.set_key("SUDOS", key)
        mmm = f"**DIHAPUS** {name} **dari Pengguna SUDO(s)**"
    await ayra.eor(mmm, time=5)


@ayra_cmd(
    pattern="[Ll][i[[s][t][s][u][d][o]$",
)
async def _(ayra):
    sudos = sudoers()
    if not sudos:
        return await ayra.eor(get_string("sudo_3"), time=5)
    msg = ""
    for i in sudos:
        try:
            name = await ayra.client.get_entity(int(i))
        except BaseException:
            name = None
        if name:
            msg += f"• {inline_mention(name)} ( `{i}` )\n"
        else:
            msg += f"• `{i}` -> Pengguna tidak valid\n"
    m = udB.get_key("SUDO") or True
    if not m:
        m = "[False](https://graph.org/Ayra-11-29)"
    return await ayra.eor(
        f"**SUDO MODE : {m}\n\nList of SUDO Users :**\n{msg}", link_preview=False
    )
