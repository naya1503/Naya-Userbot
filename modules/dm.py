# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk DM**

๏ **Perintah:** `dm` <berikan pesan/balas pesan> <username/id> <reply/type>`
◉ **Keterangan:** Kirim pesan pribadi ke pengguna.

๏ **Perintah:** `send` <balas ke pesan`
◉ **Keterangan:** Teruskan pesan tersebut ke pengguna.
"""

from . import ayra_cmd


@ayra_cmd(pattern="[dD][mM]( (.*)|$)", fullsudo=True)
async def dm(e):
    if len(e.text.split()) <= 1:
        return await e.eor(
            "`Berikan username atau id Obrolan ke mana harus mengirim.`", time=5
        )
    chat = e.text.split()[1]
    try:
        chat_id = await e.client.parse_id(chat)
    except Exception as ex:
        return await e.eor(f"`{ex}`", time=5)
    if len(e.text.split()) > 2:
        msg = e.text.split(maxsplit=2)[2]
    elif e.reply_to:
        msg = await e.get_reply_message()
    else:
        return await e.eor("`Berikan pesan atau balas ke pesan.`", time=5)
    try:
        _ = await e.client.send_message(chat_id, msg)
        n_, time = "**Pesan Berhasil Dikirim**", None
        if not _.is_private:
            n_ = f"[{n_}]({_.message_link})"
        await e.eor(n_, time=time)
    except Exception:
        await e.eor("Silakan ketik `help dm` untuk bantuan.", time=5)


@ayra_cmd(pattern="[Ss]end( (.*)|$)", fullsudo=False)
async def _(e):
    message = e.pattern_match.group(1).strip()
    if not e.reply_to_msg_id:
        return await e.eor("`Mohon balas ke pesan...`", time=5)
    if not message:
        return await e.eor("`Tidak ada pesan untuk dikirim...`", time=5)
    msg = await e.get_reply_message()
    fwd = await msg.forward_to(msg.sender_id)
    await fwd.reply(message)
    await e.eor("**Berhasil Dikirim.**", time=5)
