# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Group**

๏ **Perintah:** `getlink`
◉ **Keterangan:** Untuk mengambil link grup tersebut.

๏ **Perintah:** `buat` <g : supergroup/c : channel>
◉ **Keterangan:** Buat grup atau channel.

๏ **Perintah:** `unbanall`
◉ **Keterangan:** Unban semua pengguna.

๏ **Perintah:** `rmusers`
◉ **Keterangan:** Keluarkan pengguna secara khusus.
"""

from telethon.errors import ChatAdminRequiredError as no_admin
from telethon.tl.functions.channels import (CreateChannelRequest,
                                            GetFullChannelRequest,
                                            UpdateUsernameRequest)
from telethon.tl.functions.messages import (CreateChatRequest,
                                            ExportChatInviteRequest,
                                            GetFullChatRequest)
from telethon.tl.types import (ChannelParticipantsKicked, User,
                               UserStatusEmpty, UserStatusLastMonth,
                               UserStatusLastWeek, UserStatusOffline,
                               UserStatusOnline, UserStatusRecently)

from . import LOGS, asst, ayra_cmd, types


@ayra_cmd(
    pattern="[gG]etlink( (.*)|$)",
    groups_only=True,
    manager=True,
)
async def _(e):
    reply = await e.get_reply_message()
    match = e.pattern_match.group(1).strip()
    if reply and not isinstance(reply.sender, User):
        chat = await reply.get_sender()
    else:
        chat = await e.get_chat()
    if hasattr(chat, "username") and chat.username:
        return await e.eor(f"Username: @{chat.username}")
    request, usage, title, link = None, None, None, None
    if match:
        split = match.split(maxsplit=1)
        request = split[0] in ["r", "request"]
        title = "Created by Ayra"
        if len(split) > 1:
            match = split[1]
            spli = match.split(maxsplit=1)
            if spli[0].isdigit():
                usage = int(spli[0])
            if len(spli) > 1:
                title = spli[1]
        elif not request:
            if match.isdigit():
                usage = int(match)
            else:
                title = match
        if request and usage:
            usage = 0
    if request or title:
        try:
            r = await e.client(
                ExportChatInviteRequest(
                    e.chat_id,
                    request_needed=request,
                    usage_limit=usage,
                    title=title,
                ),
            )
        except no_admin:
            return await e.eor("`Saya bukan admin`", time=10)
        link = r.link
    else:
        if isinstance(chat, types.Chat):
            FC = await e.client(GetFullChatRequest(chat.id))
        elif isinstance(chat, types.Channel):
            FC = await e.client(GetFullChannelRequest(chat.id))
        else:
            return
        Inv = FC.full_chat.exported_invite
        if Inv and not Inv.revoked:
            link = Inv.link
    if link:
        return await e.eor(f"**Link :** {link}")
    await e.eor("`Gagal mendapatkan link...`")


@ayra_cmd(
    pattern="[Bb]uat (g|c)(?: |$)(.*)",
)
async def _(e):
    type_of_group = e.pattern_match.group(1).strip()
    group_name = e.pattern_match.group(2)
    username = None
    if " ; " in group_name:
        group_ = group_name.split(" ; ", maxsplit=1)
        group_name = group_[0]
        username = group_[1]
    xx = await e.eor("`Processing...`")
    if type_of_group == "b":
        try:
            r = await e.client(
                CreateChatRequest(
                    users=[asst.me.username],
                    title=group_name,
                ),
            )
            created_chat_id = r.chats[0].id
            result = await e.client(
                ExportChatInviteRequest(
                    peer=created_chat_id,
                ),
            )
            await xx.edit(
                f"**Berhasil Membuat [{group_name}]({result.link}) Grup Anda.**",
                link_preview=False,
            )
        except Exception as ex:
            await xx.edit(str(ex))
    elif type_of_group in ["g", "c"]:
        try:
            r = await e.client(
                CreateChannelRequest(
                    title=group_name,
                    about="Join @KynanSupport",
                    megagroup=type_of_group != "c",
                )
            )

            created_chat_id = r.chats[0].id
            if username:
                await e.client(UpdateUsernameRequest(created_chat_id, username))
                result = f"https://t.me/{username}"
            else:
                result = (
                    await e.client(
                        ExportChatInviteRequest(
                            peer=created_chat_id,
                        ),
                    )
                ).link
            await xx.edit(
                f"**Berhasil Membuat [{group_name}]({result}) Grup Anda.**",
                link_preview=False,
            )
        except Exception as ex:
            await xx.edit(str(ex))


@ayra_cmd(pattern="[Uu]nbanall$", manager=True, admins_only=True, require="ban_users")
async def _(event):
    xx = await event.eor("`Mengumpulkan akun gak guna.`")
    p = 0
    title = (await event.get_chat()).title
    async for i in event.client.iter_participants(
        event.chat_id,
        filter=ChannelParticipantsKicked,
        aggressive=True,
    ):
        try:
            await event.client.edit_permissions(event.chat_id, i, view_messages=True)
            p += 1
        except no_admin:
            pass
        except BaseException as er:
            LOGS.exception(er)
    await xx.eor(f"{title}: {p} DiUnbanned", time=5)


@ayra_cmd(
    pattern="[Rr]musers( (.*)|$)",
    groups_only=True,
    admins_only=True,
    fullsudo=True,
)
async def _(event):
    xx = await event.eor("`Processing...`")
    input_str = event.pattern_match.group(1).strip()
    p, a, b, c, d, m, n, y, w, o, q, r = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    async for i in event.client.iter_participants(event.chat_id):
        p += 1  # Total Count
        if isinstance(i.status, UserStatusEmpty):
            if "empty" in input_str:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                y += 1
        if isinstance(i.status, UserStatusLastMonth):
            if "month" in input_str:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                m += 1
        if isinstance(i.status, UserStatusLastWeek):
            if "week" in input_str:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                w += 1
        if isinstance(i.status, UserStatusOffline):
            if "offline" in input_str:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                o += 1
        if isinstance(i.status, UserStatusOnline):
            if "online" in input_str:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                q += 1
        if isinstance(i.status, UserStatusRecently):
            if "recently" in input_str:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                r += 1
        if i.bot:
            if "bot" in input_str:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                b += 1
        elif i.deleted:
            if "deleted" in input_str:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                d += 1
        elif i.status is None:
            if "none" in input_str:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                n += 1
    if input_str:
        required_string = f"**Kicked** `{c} / {p}` **Pengguna**\n\n"
    else:
        required_string = f"**Total** `{p}` **Pengguna**\n\n"
    required_string += f"  `rmusers deleted`  **••**  `{d}`\n"
    required_string += f"  `rmusers empty`  **••**  `{y}`\n"
    required_string += f"  `rmusers month`  **••**  `{m}`\n"
    required_string += f"  `rmusers week`  **••**  `{w}`\n"
    required_string += f"  `rmusers offline`  **••**  `{o}`\n"
    required_string += f"  `rmusers online`  **••**  `{q}`\n"
    required_string += f"  `rmusers recently`  **••**  `{r}`\n"
    required_string += f"  `rmusers bot`  **••**  `{b}`\n"
    required_string += f"  `rmusers none`  **••**  `{n}`"
    await xx.eor(required_string)
