# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.


import asyncio
import re
import sys
from asyncio.exceptions import TimeoutError as AsyncTimeOut
from os import execl, remove
from random import choice

try:
    from Ayra.fns.gDrive import GDriveManager
except ImportError:
    GDriveManager = None
from Ayra.fns.tools import Carbon, get_paste, telegraph_client
from Ayra.startup.loader import Loader
from telegraph import upload_file as upl
from telethon import Button, events
from telethon.tl.types import MessageMediaWebPage
from telethon.utils import get_peer_id

from . import *

# --------------------------------------------------------------------#
telegraph = telegraph_client()
GDrive = GDriveManager() if GDriveManager else None
# --------------------------------------------------------------------#---------------#


def text_to_url(event):
    """function to get media url (with|without) Webpage"""
    if isinstance(event.media, MessageMediaWebPage):
        webpage = event.media.webpage
        if not isinstance(webpage, types.WebPageEmpty) and webpage.type in ["photo"]:
            return webpage.display_url
    return event.text


# --------------------------------------------------------------------#

_buttons = {
    "otvars": {
        "text": "Pengaturan Lain nya.:",
        "buttons": [
            [
                Button.inline("Tag Logger", data="taglog"),
                Button.inline("Handler", data="hhndlr"),
            ],
            [
                Button.inline("Sudo Handler", data="shndlr"),
            ],
            [Button.inline("Kembali", data="setter")],
        ],
    },
    "apauto": {
        "text": "Ini akan otomatis menyetujui pesan keluar",
        "buttons": [
            [Button.inline("Auto Ok On", data="apon")],
            [Button.inline("Auto Ok On", data="apof")],
            [Button.inline("Kembali", data="cbs_pmcstm")],
        ],
    },
    "pmcstm": {
        "text": "Sesuaikan Pengaturan PMPERMIT Anda -",
        "buttons": [
            [
                Button.inline("PM Text", data="pmtxt"),
                Button.inline("PM Media", data="pmmed"),
            ],
            [
                Button.inline("Auto Approve PM", data="cbs_apauto"),
                Button.inline("PM Logger", data="pml"),
            ],
            [
                Button.inline("PM Limit", data="swarn"),
                Button.inline("Hapus PM Media", data="delpmmed"),
            ],
            [Button.inline("PMPermit Type", data="cbs_pmtype")],
            [Button.inline("Kembali", data="cbs_ppmset")],
        ],
    },
    "pmtype": {
        "text": "Pilih jenis PMPermit yang dibutuhkan.",
        "buttons": [
            [Button.inline("Inline", data="inpm_in")],
            [Button.inline("Normal", data="inpm_no")],
            [Button.inline("Kembali", data="cbs_pmcstm")],
        ],
    },
    "ppmset": {
        "text": "Pengaturan PMPermit:",
        "buttons": [
            [Button.inline("PMPermit On", data="pmon")],
            [Button.inline("PMPermit Off", data="pmoff")],
            [Button.inline("Costum PMPermit", data="cbs_pmcstm")],
            [Button.inline("Kembali", data="setter")],
        ],
    },
    "chatbot": {
        "text": "Dari Fitur Ini Anda dapat mengobrol dengan pengguna melalui Bot Asisten Anda.",
        "buttons": [
            [
                Button.inline("Chat Bot On", data="onchbot"),
                Button.inline("Chat Bot Off", data="ofchbot"),
            ],
            [
                Button.inline("Bot Welcome", data="bwel"),
                Button.inline("Bot Welcome Media", data="botmew"),
            ],
            [Button.inline("Bot Info Text", data="botinfe")],
            [Button.inline("Wajib Join", data="pmfs")],
            [Button.inline("Kembali", data="setter")],
        ],
    },
    "apiset": {
        "text": "Silakan Pilih API yang ingin anda atur.",
        "buttons": [
            [Button.inline("RMBG API", data="abs_rmbg")],
            [Button.inline("OPENAI API", data="abs_dapi")],
            [Button.inline("Kembali", data="setter")],
        ],
    },
}

_convo = {
    "rmbg": {
        "var": "RMBG_API",
        "name": "Remove.bg API Key",
        "text": "Masukkan API key Anda dari remove.bg.\n\nGunakan /cancel untuk membatalkan.",
        "back": "cbs_apiset",
    },
    "dapi": {
        "var": "OPENAI_API",
        "name": "Chatbot OPEN AI",
        "text": "Masukkan API key Anda dari https://platform.openai.com/account/api-keys.\n\nGunakan /cancel untuk membatalkan.",
        "back": "cbs_apiset",
    },
    "pmlgg": {
        "var": "PMLOGGROUP",
        "name": "Pm Log Group",
        "text": "Kirim id obrolan dari obrolan yang ingin Anda simpan sebagai Pm log Group.",
        "back": "pml",
    },
    "settag": {
        "var": "TAG_LOG",
        "name": "Tag Log Group",
        "text": f"Buat grup, tambahkan asisten Anda dan jadikan admin.\nDapatkan `{HNDLR}id` grup tersebut dan kirim ke sini untuk log tag.\n\nGunakan /cancel untuk membatalkan.",
        "back": "taglog",
    },
}


TOKEN_FILE = "resources/auths/auth_token.txt"


@callback(
    re.compile(
        "sndplug_(.*)",
    ),
    owner=True,
)
async def send(eve):
    key, name = (eve.data_match.group(1)).decode("UTF-8").split("_")
    thumb = "https://graph.org/file/60408fea8439e6702674d.jpg"
    await eve.answer("■ Sending ■")
    data = f"uh_{key}_"
    index = None
    if "|" in name:
        name, index = name.split("|")
    key = "plugins" if key == "Official" else key.lower()
    plugin = f"{key}/{name}.py"
    _ = f"pasta-{plugin}"
    if index is not None:
        data += f"|{index}"
        _ += f"|{index}"
    buttons = [
        [
            Button.inline(
                "« Pᴀsᴛᴇ »",
                data=_,
            )
        ],
        [
            Button.inline("Kembali", data=data),
        ],
    ]
    try:
        await eve.edit(file=plugin, thumb=thumb, buttons=buttons)
    except Exception as er:
        await eve.answer(str(er), alert=True)


heroku_api, app_name = Var.HEROKU_API, Var.HEROKU_APP_NAME


@callback("updatenow", owner=True)
async def update(eve):
    repo = Repo()
    ac_br = repo.active_branch
    if heroku_api:
        import heroku3

        try:
            heroku = heroku3.from_key(heroku_api)
            heroku_app = None
            heroku_applications = heroku.apps()
        except BaseException as er:
            LOGS.exception(er)
            return await eve.edit("`Wrong HEROKU_API.`")
        for app in heroku_applications:
            if app.name == app_name:
                heroku_app = app
        if not heroku_app:
            await eve.edit("`Wrong HEROKU_APP_NAME.`")
            repo.__del__()
            return
        await eve.edit(get_string("clst_1"))
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", f"https://api:{heroku_api}@"
        )

        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec=f"HEAD:refs/heads/{ac_br}", force=True)
        except GitCommandError as error:
            await eve.edit(f"`Ini log kesalahannya:\n{error}`")
            repo.__del__()
            return
        await eve.edit("`Berhasil Diperbarui!\nMemulai ulang, harap tunggu...`")
    else:
        await eve.edit(get_string("clst_1"))
        await bash("git pull && pip3 install -r requirements.txt")
        execl(sys.executable, sys.executable, "-m", "Ayra")


@callback(re.compile("changes(.*)"), owner=True)
async def changes(okk):
    match = okk.data_match.group(1).decode("utf-8")
    await okk.answer(get_string("clst_3"))
    repo = Repo.init()
    button = [[Button.inline("Memperbarui sekarang", data="updatenow")]]
    changelog, tl_chnglog = await gen_chlog(
        repo, f"HEAD..upstream/{repo.active_branch}"
    )
    cli = "\n\nKlik tombol di bawah untuk memperbarui!"
    if not match:
        thumb = "https://graph.org/file/60408fea8439e6702674d.jpg"
        try:
            if len(tl_chnglog) > 700:
                tl_chnglog = f"{tl_chnglog[:700]}..."
                button.append([Button.inline("Lihat Selesai", "changesall")])
            await okk.edit("• Menulis Changelog 📝 •")
            img = await Carbon(
                file_name="changelog",
                code=tl_chnglog,
                backgroundColor=choice(ATRA_COL),
                language="md",
            )
            return await okk.edit(
                f"**• Naya Userbot •**{cli}",
                file=thumb,
                buttons=button,
                force_document=True,
            )
        except Exception as er:
            LOGS.exception(er)
    changelog_str = changelog + cli
    if len(changelog_str) > 1024:
        await okk.edit(get_string("upd_4"))
        await asyncio.sleep(2)
        with open("updates.txt", "w+") as file:
            file.write(tl_chnglog)
        await okk.edit(
            get_string("upd_5"),
            file="updates.txt",
            buttons=button,
        )
        remove("updates.txt")
        return
    await okk.edit(
        changelog_str,
        buttons=button,
        parse_mode="html",
    )


@callback(
    re.compile(
        "pasta-(.*)",
    ),
    owner=True,
)
async def _(e):
    ok = (e.data_match.group(1)).decode("UTF-8")
    index = None
    if "|" in ok:
        ok, index = ok.split("|")
    with open(ok, "r") as hmm:
        _, key = await get_paste(hmm.read())
    link = f"https://spaceb.in/{key}"
    raw = f"https://spaceb.in/api/v1/documents/{key}/raw"
    if not _:
        return await e.answer(key[:30], alert=True)
    if ok.startswith("addons"):
        key = "Addons"
    elif ok.startswith("vcbot"):
        key = "VCBot"
    else:
        key = "Official"
    data = f"uh_{key}_"
    if index is not None:
        data += f"|{index}"
    await e.edit(
        "",
        buttons=[
            [Button.url("Lɪɴᴋ", link), Button.url("Rᴀᴡ", raw)],
            [Button.inline("Kembali", data=data)],
        ],
    )


@callback(re.compile("cbs_(.*)"), owner=True)
async def _edit_to(event):
    match = event.data_match.group(1).decode("utf-8")
    if data := _buttons.get(match):
        await event.edit(data["text"], buttons=data["buttons"], link_preview=False)
    else:
        return


@callback(re.compile("abs_(.*)"), owner=True)
async def convo_handler(event: events.CallbackQuery):
    match = event.data_match.group(1).decode("utf-8")
    if not _convo.get(match):
        return
    await event.delete()
    get_ = _convo[match]
    back = get_["back"]
    async with event.client.conversation(event.sender_id) as conv:
        await conv.send_message(get_["text"])
        response = conv.wait_event(events.NewMessage(chats=event.sender_id))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Dibatalkan!!",
                buttons=get_back_button(back),
            )
        await setit(event, get_["var"], themssg)
        await conv.send_message(
            f"{get_['name']} Berhasil diatur ke `{themssg}`",
            buttons=get_back_button(back),
        )


@callback("hhndlr", owner=True)
async def hndlrr(event):
    await event.delete()
    pru = event.sender_id
    var = "HNDLR"
    name = "Handler/ Trigger"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"Kirim handler/triger yang ingin anda gunakan\n [{HNDLR}] adalah handler/triger saat ini.",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            await conv.send_message(
                "Dibatalkan!!",
                buttons=get_back_button("cbs_otvars"),
            )
        elif len(themssg) > 1:
            await conv.send_message(
                "Format salah.",
                buttons=get_back_button("cbs_otvars"),
            )
        elif themssg.startswith(("/", "#", "@")):
            await conv.send_message(
                "Tidak bisa gunakan triger ini.\nCoba yang lain.",
                buttons=get_back_button("cbs_otvars"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                f"{name} Handler Diubah Ke {themssg}",
                buttons=get_back_button("cbs_otvars"),
            )


@callback("shndlr", owner=True)
async def hndlrr(event):
    await event.delete()
    pru = event.sender_id
    var = "SUDO_HNDLR"
    name = "Sudo Handler"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "Kirim handler/triger yang ingin anda gunakan untuk pengguna SUDO\n [{HNDLR}] adalah handler/triger saat ini."
        )

        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            await conv.send_message(
                "Dibatalkan!!",
                buttons=get_back_button("cbs_otvars"),
            )
        elif len(themssg) > 1:
            await conv.send_message(
                "Format salah.",
                buttons=get_back_button("cbs_otvars"),
            )
        elif themssg.startswith(("/", "#", "@")):
            await conv.send_message(
                "Tidak bisa gunakan triger ini.\nCoba yang lain.",
                buttons=get_back_button("cbs_otvars"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                f"{name} Handler Diubah Ke {themssg}",
                buttons=get_back_button("cbs_otvars"),
            )


@callback("taglog", owner=True)
async def tagloggrr(e):
    BUTTON = [
        [Button.inline("Set Tag Logger", data="abs_settag")],
        [Button.inline("Hapus Tag Logger", data="deltag")],
        get_back_button("cbs_otvars"),
    ]
    await e.edit(
        "Pilih pengaturan",
        buttons=BUTTON,
    )


@callback("deltag", owner=True)
async def _(e):
    udB.del_key("TAG_LOG")
    await e.answer("Tag Logger Berhasil Dimatikan")


@callback("inpm_in", owner=True)
async def inl_on(event):
    var = "INLINE_PM"
    await setit(event, var, "True")
    await event.edit(
        "PMPermit Diatur Ke Inline !",
        buttons=[[Button.inline("Kembali", data="cbs_pmtype")]],
    )


@callback("inpm_no", owner=True)
async def inl_on(event):
    var = "INLINE_PM"
    await setit(event, var, "False")
    await event.edit(
        "PMPermit Diatur Ke Normal !",
        buttons=[[Button.inline("Kembali", data="cbs_pmtype")]],
    )


@callback("pmtxt", owner=True)
async def name(event):
    await event.delete()
    pru = event.sender_id
    var = "PM_TEXT"
    name = "PM Text"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**PM Text**\nKirim Pesan PMText.\n\nu Anda bisa menggunakan format `{name}` `{fullname}` `{count}` `{mention}` `{username}` .",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Dibatalkan!!",
                buttons=get_back_button("cbs_pmcstm"),
            )
        if len(themssg) > 4090:
            return await conv.send_message(
                "Pesan Terlalu Panjang!",
                buttons=get_back_button("cbs_pmcstm"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"{name} Berhasil Diubah {themssg}\n\nHarap melakukan restart",
            buttons=get_back_button("cbs_pmcstm"),
        )


@callback("swarn", owner=True)
async def name(event):
    m = range(1, 10)
    tayd = [Button.inline(f"{x}", data=f"wrns_{x}") for x in m]
    lst = list(zip(tayd[::3], tayd[1::3], tayd[2::3]))
    lst.append([Button.inline("Kembali", data="cbs_pmcstm")])
    await event.edit(
        "Atur Angka PM Limit",
        buttons=lst,
    )


@callback(re.compile(b"wrns_(.*)"), owner=True)
async def set_wrns(event):
    value = int(event.data_match.group(1).decode("UTF-8"))
    if dn := udB.set_key("PMWARNS", value):
        await event.edit(
            f"PM Limit di setel ke {value}.",
            buttons=get_back_button("cbs_pmcstm"),
        )
    else:
        await event.edit("Error", buttons=get_back_button("cbs_pmcstm"))


@callback("pmmed", owner=True)
async def media(event):
    await event.delete()
    pru = event.sender_id
    var = "PMPIC"
    name = "PM Media"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**PM Media**\nSilakan Kirim Media Berupa Foto/Video/Gif\nUntuk PM Media anda.",
        )
        response = await conv.get_response()
        try:
            themssg = response.message
            if themssg == "/cancel":
                return await conv.send_message(
                    "Operasi Dibatalkan!!",
                    buttons=get_back_button("cbs_pmcstm"),
                )
        except BaseException as er:
            LOGS.exception(er)
        media = await event.client.download_media(response, "pmpc")
        if (
            not (response.text).startswith("/")
            and response.text != ""
            and (not response.media or isinstance(response.media, MessageMediaWebPage))
        ):
            url = text_to_url(response)
        elif response.sticker:
            url = response.file.id
        else:
            try:
                x = upl(media)
                url = f"https://graph.org/{x[0]}"
                remove(media)
            except BaseException as er:
                LOGS.exception(er)
                return await conv.send_message(
                    "Terminated.",
                    buttons=get_back_button("cbs_pmcstm"),
                )
        await setit(event, var, url)
        await conv.send_message(
            f"{name} Berhasil Diatur.",
            buttons=get_back_button("cbs_pmcstm"),
        )


@callback("delpmmed", owner=True)
async def dell(event):
    try:
        udB.del_key("PMPIC")
        return await event.edit(
            get_string("clst_5"), buttons=get_back_button("cbs_pmcstm")
        )
    except BaseException as er:
        LOGS.exception(er)
        return await event.edit(
            get_string("clst_4"),
            buttons=[[Button.inline("Kembali", data="setter")]],
        )


@callback("apon", owner=True)
async def apon(event):
    var = "AUTOAPPROVE"
    await setit(event, var, "True")
    await event.edit(
        "Auto OK Dihidupkan!!",
        buttons=[[Button.inline("Kembali", data="cbs_apauto")]],
    )


@callback("apof", owner=True)
async def apof(event):
    try:
        udB.set_key("AUTOAPPROVE", "False")
        return await event.edit(
            "Auto Ok Dimatikan!!",
            buttons=[[Button.inline("Kembali", data="cbs_apauto")]],
        )
    except BaseException as er:
        LOGS.exception(er)
        return await event.edit(
            get_string("clst_4"),
            buttons=[[Button.inline("Kembali", data="setter")]],
        )


@callback("pml", owner=True)
async def l_vcs(event):
    BT = (
        [Button.inline("PM Logger Off", data="pmlogof")]
        if udB.get_key("PMLOG")
        else [Button.inline("PM Logger On", data="pmlog")]
    )

    await event.edit(
        "Ini akan mengirim ke Group Private Anda",
        buttons=[
            BT,
            [Button.inline("PM Logger Grup", "abs_pmlgg")],
            [Button.inline("Kembali", data="cbs_pmcstm")],
        ],
    )


@callback("pmlog", owner=True)
async def pmlog(event):
    await setit(event, "PMLOG", "True")
    await event.edit(
        "PM Logger Dihidupkan!!",
        buttons=[[Button.inline("Kembali", data="pml")]],
    )


@callback("pmlogof", owner=True)
async def pmlogof(event):
    try:
        udB.del_key("PMLOG")
        return await event.edit(
            "PM Logger Dimatikan!!",
            buttons=[[Button.inline("Kembali", data="pml")]],
        )
    except BaseException as er:
        LOGS.exception(er)
        return await event.edit(
            get_string("clst_4"),
            buttons=[[Button.inline("Kembali", data="setter")]],
        )


@callback("pmon", owner=True)
async def pmonn(event):
    var = "PMSETTING"
    await setit(event, var, "True")
    await event.edit(
        "PMPermit Dihidupkan!!",
        buttons=[[Button.inline("Kembali", data="cbs_ppmset")]],
    )


@callback("pmoff", owner=True)
async def pmofff(event):
    var = "PMSETTING"
    await setit(event, var, "False")
    await event.edit(
        "PMPermit Dimatikan!!",
        buttons=[[Button.inline("Kembali", data="cbs_ppmset")]],
    )


@callback("botmew", owner=True)
async def hhh(e):
    async with e.client.conversation(e.chat_id) as conv:
        await conv.send_message("Kirim media apapun untuk mengatur Bot Welcome")
        msg = await conv.get_response()
        if not msg.media or msg.text.startswith("/"):
            return await conv.send_message(
                "Dibatalkan!", buttons=get_back_button("cbs_chatbot")
            )
        udB.set_key("STARTMEDIA", msg.file.id)
        await conv.send_message(
            "Berhasil Di Setel!", buttons=get_back_button("cbs_chatbot")
        )


@callback("botinfe", owner=True)
async def hhh(e):
    async with e.client.conversation(e.chat_id) as conv:
        await conv.send_message(
            "Kirim pesan untuk disetel ke Bot Info, saat pengguna menekan tombol Info di Sambutan Bot!\n\nKetik `setdb BOT_INFO_START False` untuk menghapus tombol Info atau /cancel untuk batalkan.."
        )
        msg = await conv.get_response()
        if msg.media or msg.text.startswith("/"):
            return await conv.send_message(
                "Dibatalkan!", buttons=get_back_button("cbs_chatbot")
            )
        udB.set_key("BOT_INFO_START", msg.text)
        await conv.send_message(
            "Berhasil Di Setel!", buttons=get_back_button("cbs_chatbot")
        )


@callback("pmfs", owner=True)
async def heheh(event):
    Ll = []
    err = ""
    async with event.client.conversation(event.chat_id) as conv:
        await conv.send_message(
            "Kirim ID Obrolan, yang ingin Anda gunakan untuk **Wajib Join** . Sebelum pengguna menggunakan Bot Anda\n\n• Kirim /clear untuk menonaktifkan **Wajib Join** PM Bot..\nKirim /cancel untuk batalkan.."
        )
        await conv.send_message(
            "Contoh ID Obrolan: \n`-1001234567\n-100778888`\n\nUntuk Banyak Obrolan."
        )
        try:
            msg = await conv.get_response()
        except AsyncTimeOut:
            return await conv.send_message(
                "**Waktu habis!**\nMulai dari /start kembali."
            )
        if not msg.text or msg.text.startswith("/"):
            timyork = "Dibatalkan!"
            if msg.text == "/clear":
                udB.del_key("PMBOT_FSUB")
                timyork = "Berhasil Diatur! Wajib Join Dimatikan\nKetik `restart` !"
            return await conv.send_message(
                "Dibatalkan!", buttons=get_back_button("cbs_chatbot")
            )
        for chat in msg.message.split("\n"):
            if chat.startswith("-") or chat.isdigit():
                chat = int(chat)
            try:
                CHSJSHS = await event.client.get_entity(chat)
                Ll.append(get_peer_id(CHSJSHS))
            except Exception as er:
                err += f"**{chat}** : {er}\n"
        if err:
            return await conv.send_message(err)
        udB.set_key("PMBOT_FSUB", str(Ll))
        await conv.send_message(
            "Berhasil Diatur!\nKetik `restart` !",
            buttons=get_back_button("cbs_chatbot"),
        )


@callback("bwel", owner=True)
async def name(event):
    await event.delete()
    pru = event.sender_id
    var = "STARTMSG"
    name = "Pesan Bot Welcome:"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "**Pesan Bot Welcome**\nMasukkan pesan yang ingin Anda tampilkan ketika seseorang memulai asisten Anda Bot.\\Anda Dapat menggunakan `{me}` , `{mention}` sebagai parameter\nGunakan /cancel untuk membatalkan.",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Dibatalkan!!",
                buttons=get_back_button("cbs_chatbot"),
            )
        await setit(event, var, themssg)
        await conv.send_message(
            f"{name} Diatur Ke {themssg}",
            buttons=get_back_button("cbs_chatbot"),
        )


@callback("onchbot", owner=True)
async def chon(event):
    var = "PMBOT"
    await setit(event, var, "True")
    Loader(path="assistant/pmbot.py", key="PM Bot").load_single()
    if AST_PLUGINS.get("pmbot"):
        for i, e in AST_PLUGINS["pmbot"]:
            event.client.remove_event_handler(i)
        for i, e in AST_PLUGINS["pmbot"]:
            event.client.add_event_handler(i, events.NewMessage(**e))
    await event.edit(
        "Berhasil Diaktifkan! Sekarang Anda Dapat Mengobrol Dengan Orang Melalui Bot Ini",
        buttons=[Button.inline("Kembali", data="cbs_chatbot")],
    )


@callback("ofchbot", owner=True)
async def chon(event):
    var = "PMBOT"
    await setit(event, var, "False")
    if AST_PLUGINS.get("pmbot"):
        for i, e in AST_PLUGINS["pmbot"]:
            event.client.remove_event_handler(i)
    await event.edit(
        "Berhasil Dimatikan! Sekarang Anda Tidak Dapat Mengobrol Dengan Orang Melalui Bot Ini",
        buttons=[Button.inline("Kembali", data="cbs_chatbot")],
    )
