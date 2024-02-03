# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Logo**

๏ **Perintah:** `logo` <berikan pesan>
◉ **Keterangan:** Buat logo dengan kata anda, bisa juga dengan cara membalas gambar atau font.
"""
import glob
import os
import random

from telethon.tl.types import InputMessagesFilterPhotos

try:
    from PIL import Image
except ImportError:
    Image = None
from Ayra.fns.misc import unsplashsearch
from Ayra.fns.tools import LogoHelper

from . import *


@ayra_cmd(pattern="[lL][o][g][o]( (.*)|$)")
async def logo_gen(event):
    xx = await event.eor(get_string("com_1"))
    name = event.pattern_match.group(1).strip()
    if not name:
        return await xx.eor("`Berikan kata`", time=5)
    bg_, font_ = None, None
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            if hasattr(temp.media, "document") and (
                ("font" in temp.file.mime_type)
                or (".ttf" in temp.file.name)
                or (".otf" in temp.file.name)
            ):
                font_ = await temp.download_media("resources/fonts/")
            elif "pic" in mediainfo(temp.media):
                bg_ = await temp.download_media()
    if not bg_:
        if event.client._bot:
            SRCH = [
                "blur background",
                "background",
                "neon lights",
                "nature",
                "abstract",
                "space",
                "3d render",
            ]
            res = await unsplashsearch(random.choice(SRCH), limit=1)
            bg_, _ = await download_file(res[0], "resources/downloads/logo.png")
            newimg = "resources/downloads/unsplash-temp.jpg"
            img_ = Image.open(bg_)
            img_.resize((5000, 5000)).save(newimg)
            os.remove(bg_)
            bg_ = newimg
        else:
            pics = []
            async for i in event.client.iter_messages(
                "@AllLogoHyper", filter=InputMessagesFilterPhotos
            ):
                pics.append(i)
            id_ = random.choice(pics)
            bg_ = await id_.download_media()

    if not font_:
        fpath_ = glob.glob("resources/fonts/*")
        font_ = random.choice(fpath_)
    if len(name) <= 8:
        strke = 10
    elif len(name) >= 9:
        strke = 5
    else:
        strke = 20
    name = LogoHelper.make_logo(
        bg_,
        name,
        font_,
        fill="white",
        stroke_width=strke,
        stroke_fill="black",
    )
    await xx.delete()
    await event.client.send_file(
        event.chat_id,
        file=name,
        caption=f"Logo by [{OWNER_NAME}](tg://user?id={OWNER_ID})",
        force_document=False,
    )
    os.remove(name)

    if os.path.exists(bg_):
        os.remove(bg_)
