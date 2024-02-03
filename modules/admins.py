# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

"""
✘ **Bantuan Untuk Afk**

๏ **Perintah:** `promote` <balas ke pengguna/username>
◉ **Keterangan:** Jadikan pengguna sebagai admin.

๏ **Perintah:** `promote -f` <balas ke pengguna/username>
◉ **Keterangan:** Jadikan pengguna sebagai admin akses penuh.

๏ **Perintah:** `demote` <balas ke pengguna/username>
◉ **Keterangan:** Turunkan pengguna dari admin.

๏ **Perintah:** `ban` <balas ke pengguna/username>
◉ **Keterangan:** Blokir pengguna dari grup.

๏ **Perintah:** `unban` <balas ke pengguna/username>
◉ **Keterangan:** Buka blokir pengguna dari grup.

๏ **Perintah:** `kick` <balas ke pengguna/username>
◉ **Keterangan:** Tendang pengguna dari grup.

๏ **Perintah:** `pin` <balas pesan>
◉ **Keterangan:** Sematkan pesan.

๏ **Perintah:** `unpin` <balas pesan>
◉ **Keterangan:** Lepas sematan.

๏ **Perintah:** `purge` <balas pesan>
◉ **Keterangan:** Hapus pesan dari balasan.

๏ **Perintah:** `purgeall` <balas pesan>
◉ **Keterangan:** Hapus semua pesan.

๏ **Perintah:** `purgeme` <jumlah>
◉ **Keterangan:** Hapus pesan anda menggunakan jumlah.

๏ **Perintah:** `setgpic` <balas media>
◉ **Keterangan:** Ubah foto grup.

๏ **Perintah:** `delgpic` <username grup>
◉ **Keterangan:** Hapus foto grup.

๏ **Perintah:** `del` <balas pesan>
◉ **Keterangan:** Hapus pesan yang dibalas.

๏ **Perintah:** `kickme`
◉ **Keterangan:** Keluar dari grup tersebut.
"""


from Ayra.dB import DEVS
from Ayra.kynan import register
from telethon.errors import BadRequestError
from telethon.errors.rpcerrorlist import UserIdInvalidError
from telethon.tl.functions.channels import *
from telethon.tl.functions.messages import *

from . import *


@ayra_cmd(
    pattern="^[pP][Rr][Oo][Mm][Oo][Tt][Ee]( (.*)|$)",
    admins_only=True,
    manager=True,
    require="add_admins",
    fullsudo=False,
)
async def prmte(ayra):
    xx = await ayra.eor(get_string("com_1"))
    user, rank = await get_uinfo(ayra)
    rank = rank or "Admin"
    FullRight = False
    if not user:
        return await xx.edit(get_string("pro_1"))
    if rank.split()[0] == "-f":
        try:
            rank = rank.split(maxsplit=1)[1]
        except IndexError:
            rank = "Admin"
        FullRight = True
    try:
        if FullRight:
            await ayra.client(
                EditAdminRequest(ayra.chat_id, user.id, ayra.chat.admin_rights, rank)
            )
        else:
            await ayra.client.edit_admin(
                ayra.chat_id,
                user.id,
                invite_users=True,
                ban_users=True,
                delete_messages=True,
                pin_messages=True,
                manage_call=True,
                title=rank,
            )
        await eod(
            xx, get_string("pro_2").format(inline_mention(user), ayra.chat.title, rank)
        )
    except Exception as ex:
        return await xx.edit(f"`{ex}`")


@ayra_cmd(
    pattern="^[Dd][Ee][Mm][Oo][Tt][Ee]( (.*)|$)",
    admins_only=True,
    manager=True,
    require="add_admins",
    fullsudo=False,
)
async def dmote(ayra):
    xx = await ayra.eor(get_string("com_1"))
    user, rank = await get_uinfo(ayra)
    if not rank:
        rank = "Not Admin"
    if not user:
        return await xx.edit(get_string("de_1"))
    try:
        await ayra.client.edit_admin(
            ayra.chat_id,
            user.id,
            invite_users=None,
            ban_users=None,
            delete_messages=None,
            pin_messages=None,
            manage_call=None,
            title=rank,
        )
        await eod(xx, get_string("de_2").format(inline_mention(user), ayra.chat.title))
    except Exception as ex:
        return await xx.edit(f"`{ex}`")


@ayra_cmd(
    pattern="^[bB][aA][nN]( (.*)|$)",
    admins_only=True,
    manager=True,
    require="ban_users",
    fullsudo=False,
)
async def bban(ayra):
    something = await get_uinfo(ayra)
    if not something:
        return
    user, reason = something
    if not user:
        return await eod(ayra, get_string("ban_1"))
    if user.id in DEVS:
        return await eod(ayra, get_string("ban_2"))
    try:
        await ayra.client.edit_permissions(ayra.chat_id, user.id, view_messages=False)
    except UserIdInvalidError:
        return await eod(ayra, get_string("adm_1"))
    except BadRequestError:
        return await eod(ayra, get_string("ban_3"))
    senderme = inline_mention(await ayra.get_sender())
    userme = inline_mention(user)
    text = get_string("ban_4").format(userme, senderme, ayra.chat.title)
    if reason:
        text += get_string("ban_5").format(reason)
    await eod(ayra, text)


@ayra_cmd(
    pattern="^[uU][Nn][Bb][Aa][Nn]( (.*)|$)",
    admins_only=True,
    manager=True,
    require="ban_users",
    fullsudo=False,
)
async def uunban(ayra):
    xx = await ayra.eor(get_string("com_1"))
    if ayra.text[1:].startswith("unbanall"):
        return
    something = await get_uinfo(ayra)
    if not something:
        return
    user, reason = something
    if not user:
        return await xx.edit(get_string("unban_1"))
    try:
        await ayra.client.edit_permissions(ayra.chat_id, user.id, view_messages=True)
    except UserIdInvalidError:
        return await eod(ayra, get_string("adm_1"))
    except BadRequestError:
        return await xx.edit(get_string("adm_2"))
    sender = inline_mention(await ayra.get_sender())
    text = get_string("unban_3").format(inline_mention(user), sender, ayra.chat.title)
    if reason:
        text += get_string("ban_5").format(reason)
    await xx.edit(text)


@ayra_cmd(
    pattern="^[Kk][Ii][Cc][Kk]( (.*)|$)",
    manager=True,
    require="ban_users",
    fullsudo=False,
)
async def kck(ayra):
    if "kickme" in ayra.text:
        return
    if ayra.is_private:
        return await ayra.eor("`Gunakan ini di Grup.`", time=5)
    ml = ayra.text.split(" ", maxsplit=1)[0]
    xx = await ayra.eor(get_string("com_1"))
    something = await get_uinfo(ayra)
    if not something:
        return
    user, reason = something
    if not user:
        return await xx.edit(get_string("adm_1"))
    if user.id in DEVS:
        return await xx.edit(get_string("kick_2"))
    if getattr(user, "is_self", False):
        return await xx.edit(get_string("kick_3"))
    try:
        await ayra.client.kick_participant(ayra.chat_id, user.id)
    except BadRequestError as er:
        LOGS.info(er)
        return await xx.edit(get_string("kick_1"))
    except Exception as e:
        LOGS.exception(e)
        return
    text = get_string("kick_4").format(
        inline_mention(user), inline_mention(await ayra.get_sender()), ayra.chat.title
    )
    if reason:
        text += get_string("ban_5").format(reason)
    await xx.edit(text)


@ayra_cmd(pattern="^[Pp][Ii][Nn]$", manager=True, require="pin_messages", fullsudo=True)
async def pin(msg):
    if not msg.is_reply:
        return await eor(msg, get_string("pin_1"))
    me = await msg.get_reply_message()
    if me.is_private:
        text = "`Pesan Disematkan.`"
    else:
        text = f"Berhasil Disematkan [Pesan ini]({me.message_link}) !"
    try:
        await msg.client.pin_message(msg.chat_id, me.id, notify=False)
    except BadRequestError:
        return await eor(msg, get_string("adm_2"))
    except Exception as e:
        return await eor(msg, f"**ERROR:**`{e}`")
    await eor(msg, text)


@ayra_cmd(
    pattern="^[Uu][Nn][Pp][Ii][Nn]($| (.*))",
    manager=True,
    require="pin_messages",
    fullsudo=False,
)
async def unp(ayra):
    xx = await ayra.eor(get_string("com_1"))
    ch = (ayra.pattern_match.group(1).strip()).strip()
    msg = None
    if ayra.is_reply:
        msg = ayra.reply_to_msg_id
    elif ch != "all":
        return await xx.edit(get_string("unpin_1").format(HNDLR))
    try:
        await ayra.client.unpin_message(ayra.chat_id, msg)
    except BadRequestError:
        return await xx.edit(get_string("adm_2"))
    except Exception as e:
        return await xx.edit(f"**ERROR:**`{e}`")
    await xx.edit("`Pesan Berhasil Dihapus Dari Sematan !`")


@ayra_cmd(
    pattern="^[Pp][Uu][Rr][Gg][Ee]( (.*)|$)", manager=True, require="delete_messages"
)
async def fastpurger(purg):
    match = purg.pattern_match.group(1).strip()
    try:
        ABC = purg.text[6]
    except IndexError:
        ABC = None
    if ABC and purg.text[6] in ["m", "a"]:
        return
    if not purg._client._bot and (
        (match)
        or (purg.is_reply and (purg.is_private or isinstance(purg.chat, types.Chat)))
    ):
        p = 0
        async for msg in purg.client.iter_messages(
            purg.chat_id,
            limit=int(match) if match else None,
            min_id=purg.reply_to_msg_id if purg.is_reply else None,
        ):
            await msg.delete()
            p += 0
        return await eor(purg, f"Dihapus {p} Pesan! ", time=5)
    if not purg.reply_to_msg_id:
        return await eor(purg, get_string("purge_1"), time=10)
    try:
        await purg.client.delete_messages(
            purg.chat_id, list(range(purg.reply_to_msg_id, purg.id))
        )

    except Exception as er:
        LOGS.info(er)
    await purg.eor("__Fast purge complete!__", time=5)


@ayra_cmd(
    pattern="^[Pp][Uu][Rr][Gg][Ee][Mm][Ee]( (.*)|$)",
)
@register(incoming=True, pattern=r"^Cpurgeme( (.*)|$)", from_users=DEVS)
async def fastpurgerme(purg):
    if num := purg.pattern_match.group(1).strip():
        try:
            nnt = int(num)
        except BaseException:
            await eor(purg, get_string("com_3"), time=5)
            return
        mp = 0
        async for mm in purg.client.iter_messages(
            purg.chat_id, limit=nnt, from_user="me"
        ):
            await mm.delete()
            mp += 1
        await eor(purg, f"Dihapus {mp} Pesan!", time=5)
        return
    elif not purg.reply_to_msg_id:
        return await eod(
            purg,
            "`Balas pesan untuk membersihkan atau menggunakannya seperti ``purgeme <num>`",
            time=10,
        )
    chat = await purg.get_input_chat()
    msgs = []
    async for msg in purg.client.iter_messages(
        chat,
        from_user="me",
        min_id=purg.reply_to_msg_id,
    ):
        msgs.append(msg)
    if msgs:
        await purg.client.delete_messages(chat, msgs)
    await purg.eor(
        "__Pembersihan cepat selesai!__\n**Dihapus** `"
        + str(len(msgs))
        + "` **Pesan.**",
        time=5,
    )


@ayra_cmd(
    pattern="^[Pp][Uu][Rr][Gg][Ee][Aa][Ll][Ll]$",
)
async def _(e):
    if not e.is_reply:
        return await eod(
            e,
            get_string("purgeall_1"),
        )

    msg = await e.get_reply_message()
    name = msg.sender
    try:
        await e.client.delete_messages(e.chat_id, from_user=msg.sender_id)
        await e.eor(get_string("purgeall_2").format(name.first_name), time=5)
    except Exception as er:
        return await e.eor(str(er), time=5)


@ayra_cmd(
    pattern="^[Ss][Ee][Tt][Gg][Pp][Ii][Cc]( (.*)|$)",
    admins_only=True,
    manager=True,
    require="change_info",
)
async def _(ayra):
    if not ayra.is_reply:
        return await ayra.eor("`Balas ke Media..`", time=5)
    match = ayra.pattern_match.group(1).strip()
    if not ayra.client._bot and match:
        try:
            chat = await ayra.client.parse_id(match)
        except Exception as ok:
            return await ayra.eor(str(ok))
    else:
        chat = ayra.chat_id
    reply = await ayra.get_reply_message()
    if reply.photo or reply.sticker or reply.video:
        replfile = await reply.download_media()
    elif reply.document and reply.document.thumbs:
        replfile = await reply.download_media(thumb=-1)
    else:
        return await ayra.eor("Membalas Foto atau Video..")
    mediain = mediainfo(reply.media)
    if "animated" in mediain:
        replfile = await con.convert(replfile, convert_to="mp4")
    else:
        replfile = await con.convert(
            replfile, outname="chatphoto", allowed_formats=["jpg", "png", "mp4"]
        )
    file = await ayra.client.upload_file(replfile)
    try:
        if "pic" not in mediain:
            file = types.InputChatUploadedPhoto(video=file)
        await ayra.client(EditPhotoRequest(chat, file))
        await ayra.eor("`Foto Grup Berhasil Diubah !`", time=5)
    except Exception as ex:
        await ayra.eor(f"Terjadi kesalahan.\n`{str(ex)}`", time=5)
    os.remove(replfile)


@ayra_cmd(
    pattern="^[Dd][Ee][Ll][Gg][Pp][Ii][Cc]( (.*)|$)",
    admins_only=True,
    manager=True,
    require="change_info",
)
async def _(ayra):
    match = ayra.pattern_match.group(1).strip()
    chat = match if not ayra.client._bot and match else ayra.chat_id
    try:
        await ayra.client(EditPhotoRequest(chat, types.InputChatPhotoEmpty()))
        text = "`Foto Obrolan Dihapus..`"
    except Exception as E:
        text = str(E)
    return await ayra.eor(text, time=5)


@ayra_cmd(
    pattern="^[Dd][Ee][lL]$",
    manager=True,
)
async def delete_it(delme):
    msg_src = await delme.get_reply_message()
    if not msg_src:
        return
    await msg_src.try_delete()
    await delme.try_delete()


@ayra_cmd(pattern="^[kK][Ii][Cc][Kk][Mm][Ee]$", fullsudo=False)
async def leave(ayra):
    await ayra.eor(f"`{ayra.client.me.first_name} has left this group, bye!!.`")
    await ayra.client(LeaveChannelRequest(ayra.chat_id))
