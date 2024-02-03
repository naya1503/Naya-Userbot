# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from Ayra.dB._core import LIST
from telethon.errors.rpcerrorlist import BotInlineDisabledError
from telethon.tl.custom import Button

from . import HNDLR, asst, ayra_cmd, get_string

_main_help_menu = [
    [
        Button.inline(get_string("help_4"), data="uh_Official_"),
    ],
]


@ayra_cmd(pattern="^[Hh][Ee][Ll][Pp]( (.*)|$)")
async def _help(ayra):
    plug = ayra.pattern_match.group(1).strip()
    chat = await ayra.get_chat()
    if plug:
        try:
            x = get_string("help_11").format(plug)
            for d in LIST[plug]:
                x += HNDLR + d
                x += "\n"
                x += "\n© @KynanSupport"
                await ayra.eor(x)
        except BaseException as e:
            await ayra.eor(f"{e}")
    else:
        try:
            results = await ayra.client.inline_query(asst.me.username, "help")
        except BotInlineDisabledError:
            return await ayra.eor(get_string("help_3"))
        await results[0].click(chat.id, reply_to=ayra.reply_to_msg_id)
        await ayra.delete()
