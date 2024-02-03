# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Mute**

๏ **Perintah:** `mute` <balas pesan/berikan username>
◉ **Keterangan:** Bisukan pengguna dalam obrolan saat ini.

๏ **Perintah:** `unmute` <balas pesan/berikan username>
◉ **Keterangan:** Aktifkan pengguna dalam obrolan saat ini.

๏ **Perintah:** `dmute` <balas pesan/berikan username>
◉ **Keterangan:** Bisukan pengguna dalam obrolan saat ini dengan menghapus pesan.

๏ **Perintah:** `undmute` <balas pesan/berikan username>
◉ **Keterangan:** Suarakan pengguna yang dibisukan dalam obrolan saat ini.
"""
from Ayra.dB.mute_db import is_muted, mute, unmute
from Ayra.fns.admins import ban_time
from Ayra.kynan import register
from telethon import events
from telethon.utils import get_display_name

from . import DEVS, asst, ayra_bot, ayra_cmd, eod, get_string, inline_mention


@ayra_bot.on(events.NewMessage(incoming=True))
async def watcher(event):
    if is_muted(event.chat_id, event.sender_id):
        await event.delete()
    if event.via_bot and is_muted(event.chat_id, event.via_bot_id):
        await event.delete()


@ayra_cmd(
    pattern="[Dd][m][u][t][e]( (.*)|$)",
)
@register(incoming=True, pattern=r"^\[Dd][m][u][t][e]( (.*)|$)", from_users=DEVS)
async def startmute(event):
    xx = await event.eor("`Bentar...`")
    if input_ := event.pattern_match.group(1).strip():
        try:
            userid = await event.client.parse_id(input_)
        except Exception as x:
            return await xx.edit(str(x))
    elif event.reply_to_msg_id:
        reply = await event.get_reply_message()
        userid = reply.sender_id
        if reply.out or userid in [ayra_bot.me.id, asst.me.id]:
            return await xx.eor(
                "`Anda tidak dapat membisukan diri sendiri atau bot asisten Anda.`"
            )
    elif event.is_private:
        userid = event.chat_id
    else:
        return await xx.eor("`Balas ke pengguna atau tambahkan userid mereka.`", time=5)
    chat = await event.get_chat()
    if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
        if not chat.admin_rights.delete_messages:
            return await xx.eor("`Tidak ada hak admin...`", time=5)
    elif "creator" not in vars(chat) and not event.is_private:
        return await xx.eor("`Tidak ada hak admin...`", time=5)
    if is_muted(event.chat_id, userid):
        return await xx.eor("`Pengguna ini sudah dibisukan dalam obrolan ini.`", time=5)
    mute(event.chat_id, userid)
    await xx.eor("`Berhasil dibisukan...`", time=3)


@ayra_cmd(
    pattern="[uU][n][d][m][u][t][e]( (.*)|$)",
)
@register(incoming=True, pattern=r"^\[uU][n][d][m][u][t][e]( (.*)|$)", from_users=DEVS)
async def endmute(event):
    xx = await event.eor("`Bentar...`")
    if input_ := event.pattern_match.group(1).strip():
        try:
            userid = await event.client.parse_id(input_)
        except Exception as x:
            return await xx.edit(str(x))
    elif event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.is_private:
        userid = event.chat_id
    else:
        return await xx.eor("`Balas ke pengguna atau tambahkan userid mereka.`", time=5)
    if not is_muted(event.chat_id, userid):
        return await xx.eor("`Pengguna ini tidak dibisukan dalam obrolan ini.`", time=3)
    unmute(event.chat_id, userid)
    await xx.eor("`Berhasil disuarakan...`", time=3)


@ayra_cmd(
    pattern="tmute",
    groups_only=True,
    manager=True,
)
async def _(e):
    xx = await e.eor("`Bentar...`")
    huh = e.text.split()
    try:
        tme = huh[1]
    except IndexError:
        return await xx.eor("`Berikan Waktu?`", time=5)
    try:
        input = huh[2]
    except IndexError:
        pass
    chat = await e.get_chat()
    if e.reply_to_msg_id:
        reply = await e.get_reply_message()
        userid = reply.sender_id
        name = (await reply.get_sender()).first_name
    elif input:
        userid = await e.client.parse_id(input)
        name = (await e.client.get_entity(userid)).first_name
    else:
        return await xx.eor(get_string("tban_1"), time=3)
    if userid == ayra_bot.uid:
        return await xx.eor("`Aku tidak bisa membungkam diriku sendiri.`", time=3)
    try:
        bun = ban_time(tme)
        await e.client.edit_permissions(
            chat.id,
            userid,
            until_date=bun,
            send_messages=False,
        )
        await eod(
            xx,
            f"`Berhasil Dibisukan` [{name}](tg://user?id={userid}) `in {chat.title} for {tme}`",
            time=5,
        )
    except BaseException as m:
        await xx.eor(f"`{m}`", time=5)


@ayra_cmd(
    pattern="[Uu][n][m][u][t][e]( (.*)|$)",
    admins_only=True,
    manager=True,
)
async def _(e):
    xx = await e.eor("`Bentar...`")
    input = e.pattern_match.group(1).strip()
    chat = await e.get_chat()
    if e.reply_to_msg_id:
        reply = await e.get_reply_message()
        userid = reply.sender_id
        name = (await reply.get_sender()).first_name
    elif input:
        userid = await e.client.parse_id(input)
        name = (await e.client.get_entity(userid)).first_name
    else:
        return await xx.eor(get_string("tban_1"), time=3)
    try:
        await e.client.edit_permissions(
            chat.id,
            userid,
            until_date=None,
            send_messages=True,
        )
        await eod(
            xx,
            f"`Berhasil Disuarakan` [{name}](tg://user?id={userid}) `in {chat.title}`",
            time=5,
        )
    except BaseException as m:
        await xx.eor(f"`{m}`", time=5)


@ayra_cmd(
    pattern="[mM][u][t][e]( (.*)|$)",
    admins_only=True,
    manager=True,
    require="ban_users",
)
async def _(e):
    xx = await e.eor("`Bentar...`")
    input = e.pattern_match.group(1).strip()
    chat = await e.get_chat()
    if e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
        name = get_display_name(await e.client.get_entity(userid))
    elif input:
        try:
            userid = await e.client.parse_id(input)
            name = inline_mention(await e.client.get_entity(userid))
        except Exception as x:
            return await xx.edit(str(x))
    else:
        return await xx.eor(get_string("tban_1"), time=3)
    if userid == ayra_bot.uid:
        return await xx.eor("`Aku tidak bisa membungkam diriku sendiri.`", time=3)
    try:
        await e.client.edit_permissions(
            chat.id,
            userid,
            until_date=None,
            send_messages=False,
        )
        await eod(
            xx,
            f"`Berhasil Dibisukan` {name} `in {chat.title}`",
        )
    except BaseException as m:
        await xx.eor(f"`{m}`", time=5)
