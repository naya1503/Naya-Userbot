# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Tag All**

๏ **Perintah:** `all` <berikan pesan>
◉ **Keterangan:** Tandai Anggota Grup Dengan Pesan/Tanpa Pesan

๏ **Perintah:** `emojitag` <berikan pesan>
◉ **Keterangan:** Tandai Anggota Grup Dengan Pesan/Tanpa Pesan

๏ **Perintah:** `batal`
◉ **Keterangan:** Untuk membatalkan tag all
"""

import asyncio
import random

from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import (ChannelParticipantAdmin,
                               ChannelParticipantCreator)

from . import *

spam_chats = []

emoji = "😀 😃 😄 😁 😆 😅 😂 🤣 😭 😗 😙 😚 😘 🥰 😍 🤩 🥳 🤗 🙃 🙂 ☺️ 😊 😏 😌 😉 🤭 😶 😐 😑 😔 😋 😛 😝 😜 🤪 🤔 🤨 🧐 🙄 😒 😤 😠 🤬 ☹️ 🙁 😕 😟 🥺 😳 😬 🤐 🤫 😰 😨 😧 😦 😮 😯 😲 😱 🤯 😢 😥 😓 😞 😖 😣 😩 😫 🤤 🥱 😴 😪 🌛 🌜 🌚 🌝 🎲 🧩 ♟ 🎯 🎳 🎭💕 💞 💓 💗 💖 ❤️‍🔥 💔 🤎 🤍 🖤 ❤️ 🧡 💛 💚 💙 💜 💘 💝 🐵 🦁 🐯 🐱 🐶 🐺 🐻 🐨 🐼 🐹 🐭 🐰 🦊 🦝 🐮 🐷 🐽 🐗 🦓 🦄 🐴 🐸 🐲 🦎 🐉 🦖 🦕 🐢 🐊 🐍 🐁 🐀 🐇 🐈 🐩 🐕 🦮 🐕‍🦺 🐅 🐆 🐎 🐖 🐄 🐂 🐃 🐏 🐑 🐐 🦌 🦙 🦥 🦘 🐘 🦏 🦛 🦒 🐒 🦍 🦧 🐪 🐫 🐿️ 🦨 🦡 🦔 🦦 🦇 🐓 🐔 🐣 🐤 🐥 🐦 🦉 🦅 🦜 🕊️ 🦢 🦩 🦚 🦃 🦆 🐧 🦈 🐬 🐋 🐳 🐟 🐠 🐡 🦐 🦞 🦀 🦑 🐙 🦪 🦂 🕷️ 🦋 🐞 🐝 🦟 🦗 🐜 🐌 🐚 🕸️ 🐛 🐾 🌞 🤢 🤮 🤧 🤒 🍓 🍒 🍎 🍉 🍑 🍊 🥭 🍍 🍌 🌶 🍇 🥝 🍐 🍏 🍈 🍋 🍄 🥕 🍠 🧅 🌽 🥦 🥒 🥬 🥑 🥯 🥖 🥐 🍞 🥜 🌰 🥔 🧄 🍆 🧇 🥞 🥚 🧀 🥓 🥩 🍗 🍖 🥙 🌯 🌮 🍕 🍟 🥨 🥪 🌭 🍔 🧆 🥘 🍝 🥫 🥣 🥗 🍲 🍛 🍜 🍢 🥟 🍱 🍚 🥡 🍤 🍣 🦞 🦪 🍘 🍡 🥠 🥮 🍧 🍨".split(
    " "
)


@ayra_cmd(pattern="[Aa][l][l](?: |$)(.*)")
async def mentionall(event):
    chat_id = event.chat_id
    if event.is_private:
        return await event.respond("**Jangan private bego**")

    is_admin = False
    try:
        partici_ = await ayra_bot(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        is_admin = False
    else:
        if isinstance(
            partici_.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)
        ):
            is_admin = True
    if not is_admin:
        return await event.respond("**Lu bukan admin anjeng**")

    if event.pattern_match.group(1) and event.is_reply:
        return await event.respond("**Minimal kasih pesan anjeng!!**")
    elif event.pattern_match.group(1):
        mode = "teks"
        msg = event.pattern_match.group(1)
    elif event.is_reply:
        mode = "balas"
        msg = await event.get_reply_message()
        if msg == None:
            return await event.respond("**Si anjeng dibilang kasih pesan !!**")
    else:
        return await event.respond("**Si anjeng dibilang kasih pesan !!**")

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in ayra_bot.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"🥵 [{usr.first_name}](tg://user?id={usr.id})\n"
        if usrnum == 5:
            if mode == "teks":
                txt = f"{usrtxt}\n\n{msg}"
                await ayra_bot.send_message(chat_id, txt)
            elif mode == "balas":
                await msg.reply(usrtxt)
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@ayra_cmd(pattern="[Bb][a][t][a][l](?: |$)")
async def lu_anj(event):
    if not event.chat_id in spam_chats:
        return await event.respond("**Bego orang gak ada tag all**")
    else:
        try:
            spam_chats.remove(event.chat_id)
        except:
            pass
        return await event.respond("**Iya Anjeng Nih Gua Stop.**")


@ayra_cmd(pattern="[Ee][m][o][j][i][t][a][g](?: |$)(.*)")
async def lu_kontol(event):
    chat_id = event.chat_id
    if event.is_private:
        return await event.respond("**Jangan private bego**")

    is_admin = False
    try:
        partici_ = await ayra_bot(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        is_admin = False
    else:
        if isinstance(
            partici_.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)
        ):
            is_admin = True
    if not is_admin:
        return await event.respond("**Lu bukan admin anjeng**")

    if event.pattern_match.group(1) and event.is_reply:
        return await event.respond("**Minimal kasih pesan anjeng!!**")
    elif event.pattern_match.group(1):
        mode = "teks"
        msg = event.pattern_match.group(1)
    elif event.is_reply:
        mode = "balas"
        msg = await event.get_reply_message()
        if msg == None:
            return await event.respond("**Si anjeng dibilang kasih pesan !!**")
    else:
        return await event.respond("**Si anjeng dibilang kasih pesan !!**")

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in ayra_bot.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{random.choice(emoji)}](tg://user?id={usr.id})"
        if usrnum == 5:
            if mode == "teks":
                txt = f"{usrtxt}\n\n{msg}"
                await ayra_bot.send_message(chat_id, txt)
            elif mode == "balas":
                await msg.reply(usrtxt)
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass
