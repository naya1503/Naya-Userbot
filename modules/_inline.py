# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

import re
import time
from datetime import datetime
from os import remove

from Ayra._misc._assistant import callback, in_pattern
from Ayra.dB._core import HELP, LIST
from Ayra.fns.helper import gen_chlog, time_formatter, updater
from Ayra.fns.misc import split_list
from git import Repo
from telethon import Button
from telethon.tl.types import InputWebDocument, Message
from telethon.utils import resolve_bot_file_id

from . import (HNDLR, LOGS, OWNER_NAME, InlinePlugin, asst, get_string,
               split_list, start_time, udB)
from ._help import _main_help_menu

# ================================================#

riz = get_string("riz_1")

helps = get_string("inline_1")

add_ons = udB.get_key("ADDONS")

zhelps = get_string("inline_3") if add_ons is False else get_string("inline_2")
PLUGINS = HELP.get("Official", [])
ADDONS = HELP.get("Addons", [])
upage = 0
# ============================================#

# --------------------BUTTONS--------------------#

SUP_BUTTONS = [
    [
        Button.url("• Repo •", url="https://github.com/naya1503/Naya-Userbot"),
        Button.url("• Support •", url="t.me/kynansupport"),
    ],
]

# --------------------BUTTONS--------------------#


@in_pattern("help", owner=False)
async def inline_handler(event):
    key = "Official"
    count = 0
    text = _strings.get(key, "").format(OWNER_NAME, HNDLR, len(HELP.get(key)))

    result = await event.builder.article(
        title="alive", text=text, buttons=page_num(count, key)
    )
    await event.answer([result], cache_time=0)


@in_pattern("pasta", owner=False)
async def _(event):
    ok = event.text.split("-")[1]
    link = f"https://spaceb.in/{ok}"
    raw = f"https://spaceb.in/api/v1/documents/{ok}/raw"
    result = await event.builder.article(
        title="Paste",
        text="Pasted to Spacebin 🌌",
        buttons=[
            [
                Button.url("SpaceBin", url=link),
                Button.url("Raw", url=raw),
            ],
        ],
    )
    await event.answer([result])


@callback("ownr", owner=False)
async def setting(event):
    z = []
    for x in LIST.values():
        z.extend(x)
    await event.edit(
        get_string("inline_4").format(
            OWNER_NAME,
            len(HELP.get("Official", [])),
            len(z),
        ),
        link_preview=False,
        buttons=[
            [
                Button.inline("•Pɪɴɢ•", data="pkng"),
                Button.inline("•Uᴘᴛɪᴍᴇ•", data="upp"),
            ],
            [
                Button.inline("•Stats•", data="alive"),
                Button.inline("•Uᴘᴅᴀᴛᴇ•", data="doupdate"),
            ],
            [Button.inline("❮", data="open")],
        ],
    )


_strings = {"Official": helps, "Addons": zhelps, "VCBot": get_string("inline_6")}


@callback(re.compile("uh_(.*)"), owner=False)
async def help_func(ayra):
    key, count = ayra.data_match.group(1).decode("utf-8").split("_")
    if "|" in count:
        _, count = count.split("|")
    count = int(count) if count else 0
    text = _strings.get(key, "").format(OWNER_NAME, HNDLR, len(HELP.get(key)))
    await ayra.edit(text, buttons=page_num(count, key), link_preview=False)


@callback(re.compile("uplugin_(.*)"), owner=False)
async def uptd_plugin(event):
    key, file = event.data_match.group(1).decode("utf-8").split("_")
    index = None
    if "|" in file:
        file, index = file.split("|")
    key_ = HELP.get(key, [])
    hel_p = f"Plugin Name - `{file}`\n"
    help_ = ""
    try:
        for i in key_[file]:
            help_ += i
    except BaseException:
        if file in LIST:
            help_ = get_string("help_11").format(file)
            for d in LIST[file]:
                help_ += HNDLR + d
                help_ += "\n"
    if not help_:
        help_ = f"{file} has no Detailed Help!"
    help_ += "\n© @KynanSupport"
    data = f"uh_{key}_"
    if index is not None:
        data += f"|{index}"
    buttons = [[Button.inline("❮", data=data)]]
    try:
        await event.edit(help_, buttons=buttons)
    except Exception as er:
        LOGS.exception(er)
        help = f"Do `{HNDLR}help {key}` to get list of commands."
        await event.edit(help, buttons=buttons)


@callback(data="doupdate", owner=False)
async def _(event):
    if not await updater():
        return await event.answer(get_string("inline_9"), cache_time=0, alert=True)
    repo = Repo.init()
    changelog, tl_chnglog = await gen_chlog(
        repo, f"HEAD..upstream/{repo.active_branch}"
    )
    changelog_str = changelog + "\n\n" + get_string("inline_8")
    if len(changelog_str) > 1024:
        await event.edit(get_string("upd_4"))
        with open("ayra_updates.txt", "w+") as file:
            file.write(tl_chnglog)
        await event.edit(
            get_string("upd_5"),
            file="ayra_updates.txt",
            buttons=[
                [Button.inline("Update Sekarang", data="updatenow")],
                [Button.inline("❮", data="ownr")],
            ],
        )
        remove("ayra_updates.txt")
    else:
        await event.edit(
            changelog_str,
            buttons=[
                [Button.inline("Update Sekarang", data="updatenow")],
                [Button.inline("❮", data="ownr")],
            ],
            parse_mode="html",
        )


@callback(data="pkng", owner=False)
async def _(event):
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds
    pin = f"🌋Pɪɴɢ = {ms} microseconds"
    await event.answer(pin, cache_time=0, alert=True)


@callback(data="upp", owner=False)
async def _(event):
    uptime = time_formatter((time.time() - start_time) * 1000)
    pin = f"🙋Uᴘᴛɪᴍᴇ = {uptime}"
    await event.answer(pin, cache_time=0, alert=True)


@callback(data="inlone", owner=False)
async def _(e):
    _InButtons = [
        Button.switch_inline(_, query=InlinePlugin[_], same_peer=True)
        for _ in list(InlinePlugin.keys())
    ]
    InButtons = split_list(_InButtons, 2)

    button = InButtons.copy()
    button.append(
        [
            Button.inline("❮", data="open"),
        ],
    )
    await e.edit(buttons=button, link_preview=False)


@callback(data="open", owner=False)
async def opner(event):
    z = []
    for x in LIST.values():
        z.extend(x)
    await event.edit(
        get_string("inline_4").format(
            len(HELP.get("Official", [])),
            len(z),
        ),
        buttons=_main_help_menu,
        link_preview=False,
    )


@callback(data="close", owner=False)
async def on_plug_in_callback_query_handler(event):
    await event.edit(
        get_string("inline_5"),
        buttons=Button.inline("Buka", data="open"),
    )


def page_num(index, key):
    rows = udB.get_key("HELP_ROWS") or 3
    cols = udB.get_key("HELP_COLUMNS") or 2
    loaded = HELP.get(key, [])
    emoji = udB.get_key("EMOJI_IN_HELP") or ""
    List = [
        Button.inline(f"{emoji} {x} {emoji}", data=f"uplugin_{key}_{x}|{index}")
        for x in sorted(loaded)
    ]
    all_ = split_list(List, cols)
    fl_ = split_list(all_, rows)
    try:
        new_ = fl_[index]
    except IndexError:
        new_ = fl_[0] if fl_ else []
        index = 0
    if index == 0 and len(fl_) == 1:
        new_.append([Button.inline("Kembali", data="open")])
    else:
        new_.append(
            [
                Button.inline(
                    "❮",
                    data=f"uh_{key}_{index-1}",
                ),
                Button.inline(
                    "❯",
                    data=f"uh_{key}_{index+1}",
                ),
            ]
        )
    return new_


# --------------------------------------------------------------------------------- #


STUFF = {}


@in_pattern("stf(.*)", owner=False)
async def ibuild(e):
    n = e.pattern_match.group(1).strip()
    builder = e.builder
    if not (n and n.isdigit()):
        return
    ok = STUFF.get(int(n))
    txt = ok.get("msg")
    pic = ok.get("media")
    btn = ok.get("button")
    if not (pic or txt):
        txt = "Mmkkkkkk"
    if pic:
        try:
            include_media = True
            mime_type, _pic = None, None
            cont, results = None, None
            try:
                ext = str(pic).split(".")[-1].lower()
            except BaseException:
                ext = None
            if ext in ["img", "jpg", "png"]:
                _type = "photo"
                mime_type = "image/jpg"
            elif ext in ["mp4", "mkv", "gif"]:
                mime_type = "video/mp4"
                _type = "gif"
            else:
                try:
                    if "telethon.tl.types" in str(type(pic)):
                        _pic = pic
                    else:
                        _pic = resolve_bot_file_id(pic)
                except BaseException:
                    pass
                if _pic:
                    results = [
                        await builder.document(
                            _pic,
                            title="Ayra Op",
                            text=txt,
                            description="@Riizzvbss",
                            buttons=btn,
                            link_preview=False,
                        )
                    ]
                else:
                    _type = "article"
                    include_media = False
            if not results:
                if include_media:
                    cont = InputWebDocument(pic, 0, mime_type, [])
                results = [
                    await builder.article(
                        title="Ayra Op",
                        type=_type,
                        text=txt,
                        description="@Riizzvbss",
                        include_media=include_media,
                        buttons=btn,
                        thumb=cont,
                        content=cont,
                        link_preview=False,
                    )
                ]
            return await e.answer(results)
        except Exception as er:
            LOGS.exception(er)
    result = [
        await builder.article("Ayra Op", text=txt, link_preview=False, buttons=btn)
    ]
    await e.answer(result)


async def something(e, msg, media, button, reply=True, chat=None):
    if e.client._bot:
        return await e.reply(msg, file=media, buttons=button)
    num = len(STUFF) + 1
    STUFF.update({num: {"msg": msg, "media": media, "button": button}})
    try:
        res = await e.client.inline_query(asst.me.username, f"stf{num}")
        return await res[0].click(
            chat or e.chat_id,
            reply_to=bool(isinstance(e, Message) and reply),
            hide_via=True,
            silent=True,
        )

    except Exception as er:
        LOGS.exception(er)
