# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Chatbot**

๏ **Perintah:** `ai` <berikan pertanyaan>
◉ **Keterangan:** Sangat berguna untuk kebutuhan.

๏ **Perintah:** `img` <query>
◉ **Keterangan:** Mencari gambar menggunakan ai.
"""

from . import LOGS, ayra_cmd, eod, inline_mention, udB
from .database.ai import OpenAi, get_chatbot_reply


@ayra_cmd(pattern="ai( (.*)|$)")
async def openai(event):
    question = event.pattern_match.group(2)
    if not question:
        await event.eor("`Mohon berikan pertanyaan untuk menggunakan AI.`")
        return
    msg = await event.eor("`Processing...`")
    try:
        response = OpenAi().text(question)
        await msg.eor(f"**Q:** {question}\n\n**A:** {response}")
    except Exception as e:
        await msg.eor(f"**Q:** {question}\n\n**A:** `Error: {e}`")


@ayra_cmd(pattern="img( (.*)|$)")
async def imge(event):
    question = event.pattern_match.group(2)
    if not question:
        await event.eor("`Mohon berikan pertanyaan untuk menggunakan AI.`")
        return
    msg = await event.eor("`Processing...`")
    try:
        response = OpenAi().photo(question)
        await event.client.send_file(
            event.chat_id, file=response, reply_to=event.message.id
        )
        await msg.delete()
    except Exception as error:
        await event.eor(str(error))


@ayra_cmd(pattern="repai")
async def im_lonely_chat_with_me(event):
    if event.reply_to:
        message = (await event.get_reply_message()).message
    else:
        try:
            message = event.text.split(" ", 1)[1]
        except IndexError:
            return await eod(
                event, "Balas ke pesan pengguna atau beri saya id/username", time=10
            )
    reply_ = await get_chatbot_reply(message=message)
    await event.eor(reply_)


@ayra_cmd(pattern="addai")
async def add_chatBot(event):
    await chat_bot_fn(event, type_="add")


@ayra_cmd(pattern="remai")
async def rem_chatBot(event):
    await chat_bot_fn(event, type_="remov")


@ayra_cmd(pattern="listai")
async def lister(event):
    key = udB.get_key("CHATBOT_USERS") or {}
    users = key.get(event.chat_id, [])
    if not users:
        return await event.eor("`Belum ada pengguna yang ditambahkan AI.`", time=5)
    msg = "**Daftar Total Pengguna yang Diaktifkan AI Dalam Obrolan Ini :**\n\n"
    for i in users:
        try:
            user = await event.client.get_entity(int(i))
            user = inline_mention(user)
        except BaseException:
            user = f"`{i}`"
        msg += f"• {user}\n"
    await event.eor(msg, link_preview=False)


async def chat_bot_fn(event, type_):
    if event.reply_to:
        user_ = (await event.get_reply_message()).sender
    else:
        temp = event.text.split(maxsplit=1)
        try:
            user_ = await event.client.get_entity(await event.client.parse_id(temp[1]))
        except BaseException as er:
            LOGS.exception(er)
            user_ = event.chat if event.is_private else None
    if not user_:
        return await eod(
            event,
            "Balas ke pesan pengguna atau beri saya id/username untuk menambahkan ChatBot AI!",
        )
    key = udB.get_key("CHATBOT_USERS") or {}
    chat = event.chat_id
    user = user_.id
    if type_ == "add":
        if key.get(chat):
            if user not in key[chat]:
                key[chat].append(user)
        else:
            key.update({chat: [user]})
            await event.eor(f"**Ditambahkan untuk CHATBOT:**\n{inline_mention(user_)}")
    elif type_ == "remov":
        if key.get(chat):
            if user in key[chat]:
                key[chat].remove(user)
            if chat in key and not key[chat]:
                del key[chat]
                await event.eor(f"**Dihapus untuk CHATBOT:**\n{inline_mention(user_)}")
    udB.set_key("CHATBOT_USERS", key)
