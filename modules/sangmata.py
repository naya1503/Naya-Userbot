# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Sangmata**

๏ **Perintah:** `id` <balas pesan/berikan username/none>
◉ **Keterangan:** Dapatkan ID

๏ **Perintah:** `sg` <balas pesan/berikan user id>
◉ **Keterangan:** Dapatkan History Pengguna.
"""
from asyncio.exceptions import TimeoutError as AsyncTimeout

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from htmlwebshot import WebShot
except ImportError:
    WebShot = None
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import ayra_cmd, get_string


@ayra_cmd(
    pattern="[Ii]d( (.*)|$)",
    manager=True,
)
async def _(event):
    ayra = event
    if match := event.pattern_match.group(1).strip():
        try:
            ids = await event.client.parse_id(match)
        except Exception as er:
            return await event.eor(str(er))
        return await event.eor(
            f"**Chat ID:**  `{event.chat_id}`\n**User ID:**  `{ids}`"
        )
    data = f"**Current Chat ID:**  `{event.chat_id}`"
    if event.reply_to_msg_id:
        event = await event.get_reply_message()
        data += f"\n**From User ID:**  `{event.sender_id}`"
    if event.media:
        bot_api_file_id = event.file.id
        data += f"\n**Bot API File ID:**  `{bot_api_file_id}`"
    data += f"\n**Msg ID:**  `{event.id}`"
    await ayra.eor(data)


@ayra_cmd(
    pattern="[Ss]g( (.*)|$)",
)
async def lastname(steal):
    mat = steal.pattern_match.group(1).strip()
    if not steal.is_reply and not mat:
        return await steal.eor("`Balas Ke Pengguna/Berikan Username atau ID.`")
    if mat:
        try:
            user_id = await steal.client.parse_id(mat)
        except ValueError:
            user_id = mat
    message = await steal.get_reply_message()
    if message:
        user_id = message.sender.id
    chat = "@SangMata_beta_bot"
    id = f"{user_id}"
    lol = await steal.eor(get_string("com_1"))
    try:
        async with steal.client.conversation(chat) as conv:
            try:
                msg = await conv.send_message(id)
                response = await conv.get_response()
            except YouBlockedUserError:
                return await lol.edit("Buka Blokir @SangMata_beta_bot dan Coba Lagi.")
            if response and response.text == "No":
                await lol.edit("No records found for this user")
                await steal.client.delete_messages(conv.chat_id, [msg.id, response.id])
            elif response.text.startswith("History"):
                await lol.edit(response.message)
            else:
                await lol.edit(response.message)
            await steal.client.delete_messages(
                conv.chat_id,
                [msg.id, response.id],
            )
    except AsyncTimeout:
        await lol.edit("Error: @SangMata_beta_bot is not responding!.")
