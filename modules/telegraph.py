# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Telegraph**

๏ **Perintah:** `tg`
◉ **Keterangan:** Upload File Atau Teks Ke Telegraph
"""

import os
import pathlib

try:
    from PIL import Image
except ImportError:
    Image = None


try:
    from telegraph import upload_file as uf
except ImportError:
    uf = None


from . import Image, Telegraph, ayra_cmd, bash, get_string, mediainfo

# =================================================================#

TMP_DOWNLOAD_DIRECTORY = "resources/downloads/"

_copied_msg = {}


@ayra_cmd(
    pattern="[tT][gG]( (.*)|$)",
)
async def telegraphcmd(event):
    xx = await event.eor(get_string("com_1"))
    match = event.pattern_match.group(1).strip() or "Ayra"
    reply = await event.get_reply_message()
    if not reply:
        return await xx.eor("`Balas Ke Pesan.`")
    if not reply.media and reply.message:
        content = reply.message
    else:
        getit = await reply.download_media()
        dar = mediainfo(reply.media)
        if dar == "sticker":
            file = f"{getit}.png"
            Image.open(getit).save(file)
            os.remove(getit)
            getit = file
        elif dar.endswith("animated"):
            file = f"{getit}.gif"
            await bash(f"lottie_convert.py '{getit}' {file}")
            os.remove(getit)
            getit = file
        if "document" not in dar:
            try:
                nn = f"https://graph.org{uf(getit)[0]}"
                amsg = f"Uploaded to [Telegraph]({nn}) !"
            except Exception as e:
                amsg = f"Error : {e}"
            os.remove(getit)
            return await xx.eor(amsg)
        content = pathlib.Path(getit).read_text()
        os.remove(getit)
    makeit = Telegraph.create_page(title=match, content=[content])
    await xx.eor(
        f"Pasted to Telegraph : [Telegraph]({makeit['url']})", link_preview=False
    )
