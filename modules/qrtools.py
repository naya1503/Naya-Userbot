# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk QR Tools**

๏ **Perintah:** `qrcode` <balas pesan>
◉ **Keterangan:** Membuat qrcode teks.

๏ **Perintah:** `addqr` <balas pesan>
◉ **Keterangan:** Membuat qr teks dan menambahkannya ke gambar.

๏ **Perintah:** `qrdecode` <balas pesan> <jumlah> <warna>
◉ **Keterangan:** Menerjemahkan QR.

"""
import os

from Ayra import AyConfig

try:
    import cv2
except ImportError:
    cv2 = None

import qrcode
from PIL import Image
from telethon.tl.types import MessageMediaDocument as doc
from telethon.tl.types import MessageMediaPhoto as photu

from . import ayra_bot, ayra_cmd, check_filename, get_string


@ayra_cmd(pattern="[qQ]rcode( (.*)|$)")
async def cd(e):
    reply = await e.get_reply_message()
    msg = e.pattern_match.group(1).strip()
    if reply and reply.text:
        msg = reply.text
    elif not msg:
        return await e.eor("`Berikan Beberapa Teks atau Balas Pesan", time=5)
    default, cimg = AyConfig.thumb, None
    if reply and (reply.sticker or reply.photo):
        cimg = await reply.download_media()
    elif ayra_bot.me.photo and not ayra_bot.me.photo.has_video:
        cimg = await e.client.get_profile_photos(ayra_bot.uid, limit=1)[0]

    kk = await e.eor(get_string("com_1"))
    img = cimg or default
    ok = Image.open(img)
    logo = ok.resize((60, 60))
    cod = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    cod.add_data(msg)
    cod.make()
    imgg = cod.make_image().convert("RGB")
    pstn = ((imgg.size[0] - logo.size[0]) // 2, (imgg.size[1] - logo.size[1]) // 2)
    imgg.paste(logo, pstn)
    newname = check_filename("qr.jpg")
    imgg.save(newname)
    await e.client.send_file(e.chat_id, newname, supports_streaming=True)
    await kk.delete()
    os.remove(newname)
    if cimg:
        os.remove(cimg)


@ayra_cmd(pattern="[Aa]ddqr( (.*)|$)")
async def qrwater(e):
    msg = e.pattern_match.group(1).strip()
    r = await e.get_reply_message()
    if isinstance(r.media, photu):
        dl = await e.client.download_media(r.media)
    elif isinstance(r.media, doc):
        dl = await e.client.download_media(r, thumb=-1)
    else:
        return await e.eor("`Balas Media Apa Saja dan Berikan Teks`", time=5)
    kk = await e.eor(get_string("com_1"))
    img_bg = Image.open(dl)
    qr = qrcode.QRCode(box_size=5)
    qr.add_data(msg)
    qr.make()
    img_qr = qr.make_image()
    pos = (img_bg.size[0] - img_qr.size[0], img_bg.size[1] - img_qr.size[1])
    img_bg.paste(img_qr, pos)
    img_bg.save(dl)
    await e.client.send_file(e.chat_id, dl, supports_streaming=True)
    await kk.delete()
    os.remove(dl)


@ayra_cmd(pattern="[qQ]rdecode$")
async def decod(e):
    r = await e.get_reply_message()
    if not (r and r.media):
        return await e.eor("`Balas ke Qrcode Media`", time=5)
    kk = await e.eor(get_string("com_1"))
    if isinstance(r.media, photu):
        dl = await r.download_media()
    elif isinstance(r.media, doc):
        dl = await r.download_media(thumb=-1)
    else:
        return
    im = cv2.imread(dl)
    try:
        det = cv2.QRCodeDetector()
        tx, y, z = det.detectAndDecode(im)
        await kk.edit("**Teks yang Didekodekan:\n\n**" + tx)
    except BaseException:
        await kk.edit("`Balas Ke Media di mana gambar Qr hadir.`")
    os.remove(dl)
