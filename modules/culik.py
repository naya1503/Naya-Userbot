# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Culik**

๏ **Perintah:** `invite` <id pengguna>
◉ **Keterangan:** Culik 1 member.

๏ **Perintah:** `inviteall` <username grup>
◉ **Keterangan:** Culik banyak member dari grup tersebut.

◉ **Notes:** Fitur Ini Dilarang Keras Untuk IDC 5 & 6 Karena Akun Anda Akan Ter-Deak.
"""


from telethon import functions
from telethon.errors import (ChannelInvalidError, ChannelPrivateError,
                             ChannelPublicGroupNaError)
from telethon.tl.functions.channels import (GetFullChannelRequest,
                                            InviteToChannelRequest)
from telethon.tl.functions.messages import GetFullChatRequest

from . import *


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await eor(event, "`Grup tidak ditemukan...`")
            return None
        except ChannelPrivateError:
            await eod(event, "`Sepertinya Grup Private...`")

            return None
        except ChannelPublicGroupNaError:
            await eod(event, "`Grup tidak ditemukan...`")
            return None
        except (TypeError, ValueError):
            await eod(event, "`Grup tidak ditemukan...`")
            return None
    return chat_info


@ayra_cmd(pattern="[Ii][n][v][i][t][e](?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await eor(
            event,
            "Gunakan format `invite` pengguna ke grup chat, bukan ke Pesan Pribadi.",
        )

    else:
        if not event.is_channel and event.is_group:
            for user_id in to_add_users.split():
                try:
                    if user_id.isdigit():
                        user_id = int(user_id)
                    await event.client(
                        functions.messages.AddChatUserRequest(
                            chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000
                        )
                    )
                except Exception as e:
                    return await eor(event, f"**Error** : `{e}`.")
        else:
            for user_id in to_add_users.split():
                try:
                    if user_id.isdigit():
                        user_id = int(user_id)
                    await event.client(
                        functions.channels.InviteToChannelRequest(
                            channel=event.chat_id, users=[user_id]
                        )
                    )
                except Exception as e:
                    return await eor(event, f"**Error** : `{e}`.")

        await eor(event, "`Sukses Nyulik Untung Ga Deak...`")


# inviteall Ported By @VckyouuBitch
# From Geez - Projects <https://github.com/vckyou/Geez-UserBot>
# Copyright © Team Geez - Project


@ayra_cmd(pattern="[Ii][n][v][i][t][e][a][l][l] ?(.*)")
async def get_users(event):
    ajgg = event.text[11:]
    chat_ajgg = ajgg.lower()
    restricted = ["@KynanSupport", "@kynansupport"]
    if chat_ajgg in restricted:
        await eor(event, "**Dilarang nyulik member dari sana om.**")
        await event.client.send_message(-1001812143750, "**Mo nyulik kaga bisa.**")

        return
    if not ajgg:
        return await eor(event, "`Berikan username grup...`")

    ayraa = await eor(event, "`Processing....`")
    babi = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await ayraa.edit("**Tidak bisa Menambahkan Member di sini.**")

    s = 0
    f = 0
    error = "None"
    await ayraa.edit("`Processing...`")
    async for user in event.client.iter_participants(babi.full_chat.id):
        try:
            await event.client(InviteToChannelRequest(channel=chat, users=[user.id]))
            s += 1
            await ayraa.edit(
                f"`Processing...`\n\n• **Menambahkan** `{s}` **orang** \n• **Gagal Menambahkan** `{f}` **orang**\n\n** Error:** `{error}`"
            )
        except Exception as e:
            error = str(e)
            f += 1
    return await ayraa.edit(
        f"**Terminal Selesai** \n\n• **Berhasil Menambahkan** `{s}` **orang** \n• **Gagal Menambahkan** `{f}` **orang**"
    )
